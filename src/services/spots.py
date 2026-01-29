from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from src.models import Image, Spot, User
from src.schemas import SpotCreate, SpotUpdate
from src.services.geocoding import geocoding_service


class SpotService:
    async def create(self, db: Session, spot_in: SpotCreate, user: User) -> Spot:
        """Create a new spot."""
        spot_data = spot_in.model_dump()

        if not spot_data.get("address"):
            address = await geocoding_service.reverse_geocode(
                spot_data["latitude"], spot_data["longitude"]
            )
            spot_data["address"] = address

        spot = Spot(**spot_data, user_id=user.id)
        db.add(spot)
        db.commit()
        db.refresh(spot)

        return self.get_by_id(db, spot.id)

    def get_by_id(self, db: Session, spot_id: int) -> Spot | None:
        """Get a spot by ID with related data."""
        stmt = (
            select(Spot)
            .options(joinedload(Spot.user), joinedload(Spot.images))
            .where(Spot.id == spot_id)
        )
        return db.execute(stmt).unique().scalar_one_or_none()

    def get_list(
        self,
        db: Session,
        page: int = 1,
        size: int = 20,
        category: str | None = None,
        min_rating: float | None = None,
        user_id: int | None = None,
    ) -> tuple[list[Spot], int]:
        """Get paginated list of spots with filters."""
        stmt = select(Spot).options(joinedload(Spot.user), joinedload(Spot.images))

        if category:
            stmt = stmt.where(Spot.category == category)
        if min_rating is not None:
            stmt = stmt.where(Spot.rating >= min_rating)
        if user_id:
            stmt = stmt.where(Spot.user_id == user_id)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.execute(count_stmt).scalar() or 0

        stmt = stmt.order_by(Spot.created_at.desc())
        stmt = stmt.offset((page - 1) * size).limit(size)

        spots = db.execute(stmt).unique().scalars().all()
        return list(spots), total

    def update(self, db: Session, spot: Spot, spot_in: SpotUpdate) -> Spot:
        """Update a spot."""
        update_data = spot_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(spot, field, value)
        db.commit()
        db.refresh(spot)
        return self.get_by_id(db, spot.id)

    def delete(self, db: Session, spot: Spot) -> None:
        """Delete a spot."""
        db.delete(spot)
        db.commit()

    def add_image(
        self, db: Session, spot: Spot, url: str, object_name: str, is_primary: bool = False
    ) -> Image:
        """Add an image to a spot."""
        if is_primary:
            for img in spot.images:
                img.is_primary = False

        image = Image(url=url, object_name=object_name, is_primary=is_primary, spot_id=spot.id)
        db.add(image)
        db.commit()
        db.refresh(image)
        return image

    def get_image_by_id(self, db: Session, image_id: int) -> Image | None:
        """Get an image by ID."""
        return db.execute(select(Image).where(Image.id == image_id)).scalar_one_or_none()

    def delete_image(self, db: Session, image: Image) -> None:
        """Delete an image."""
        db.delete(image)
        db.commit()


spot_service = SpotService()
