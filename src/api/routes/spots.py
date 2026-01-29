import math

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.core.exceptions import BadRequestException, ForbiddenException, NotFoundException
from src.db.session import get_db
from src.models import User
from src.schemas import ImageResponse, SpotCreate, SpotResponse, SpotsResponse, SpotUpdate
from src.services import spot_service, storage_service

router = APIRouter()


@router.post("", response_model=SpotResponse, status_code=201)
async def create_spot(
    spot_in: SpotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SpotResponse:
    """Create a new spot."""
    spot = await spot_service.create(db, spot_in, current_user)
    return spot


@router.get("", response_model=SpotsResponse)
def list_spots(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category: str | None = None,
    min_rating: float | None = Query(None, ge=0, le=5),
    user_id: int | None = None,
    db: Session = Depends(get_db),
) -> SpotsResponse:
    """List spots with optional filters."""
    spots, total = spot_service.get_list(
        db, page=page, size=size, category=category, min_rating=min_rating, user_id=user_id
    )
    return SpotsResponse(
        items=spots,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total > 0 else 0,
    )


@router.get("/{spot_id}", response_model=SpotResponse)
def get_spot(spot_id: int, db: Session = Depends(get_db)) -> SpotResponse:
    """Get a spot by ID."""
    spot = spot_service.get_by_id(db, spot_id)
    if not spot:
        raise NotFoundException("Spot not found")
    return spot


@router.patch("/{spot_id}", response_model=SpotResponse)
def update_spot(
    spot_id: int,
    spot_in: SpotUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SpotResponse:
    """Update a spot."""
    spot = spot_service.get_by_id(db, spot_id)
    if not spot:
        raise NotFoundException("Spot not found")
    if spot.user_id != current_user.id:
        raise ForbiddenException("Not authorized to update this spot")
    return spot_service.update(db, spot, spot_in)


@router.delete("/{spot_id}", status_code=204)
def delete_spot(
    spot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a spot."""
    spot = spot_service.get_by_id(db, spot_id)
    if not spot:
        raise NotFoundException("Spot not found")
    if spot.user_id != current_user.id:
        raise ForbiddenException("Not authorized to delete this spot")

    for image in spot.images:
        storage_service.delete_image(image.object_name)

    spot_service.delete(db, spot)


@router.post("/{spot_id}/images", response_model=ImageResponse, status_code=201)
def upload_image(
    spot_id: int,
    file: UploadFile = File(...),
    is_primary: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ImageResponse:
    """Upload an image to a spot."""
    spot = spot_service.get_by_id(db, spot_id)
    if not spot:
        raise NotFoundException("Spot not found")
    if spot.user_id != current_user.id:
        raise ForbiddenException("Not authorized to add images to this spot")

    if len(spot.images) >= 5:
        raise BadRequestException("Maximum 5 images per spot")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise BadRequestException("File must be an image")

    file_data = file.file.read()
    object_name, url = storage_service.upload_image(file_data, file.content_type)

    return spot_service.add_image(db, spot, url, object_name, is_primary)


@router.delete("/images/{image_id}", status_code=204)
def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete an image."""
    image = spot_service.get_image_by_id(db, image_id)
    if not image:
        raise NotFoundException("Image not found")

    spot = spot_service.get_by_id(db, image.spot_id)
    if not spot or spot.user_id != current_user.id:
        raise ForbiddenException("Not authorized to delete this image")

    storage_service.delete_image(image.object_name)
    spot_service.delete_image(db, image)
