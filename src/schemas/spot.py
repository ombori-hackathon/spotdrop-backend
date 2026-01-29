from datetime import datetime

from pydantic import BaseModel, Field

from src.schemas.image import ImageResponse
from src.schemas.user import UserResponse


class SpotCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str | None = None
    category: str = Field(..., max_length=50)
    rating: float | None = Field(None, ge=0, le=5)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: str | None = Field(None, max_length=500)
    best: str | None = Field(None, max_length=200)
    best_time: str | None = Field(None, max_length=100)
    price_level: int | None = Field(None, ge=1, le=4)


class SpotUpdate(BaseModel):
    title: str | None = Field(None, max_length=200)
    description: str | None = None
    category: str | None = Field(None, max_length=50)
    rating: float | None = Field(None, ge=0, le=5)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    address: str | None = Field(None, max_length=500)
    best: str | None = Field(None, max_length=200)
    best_time: str | None = Field(None, max_length=100)
    price_level: int | None = Field(None, ge=1, le=4)


class SpotResponse(BaseModel):
    id: int
    title: str
    description: str | None
    category: str
    rating: float | None
    latitude: float
    longitude: float
    address: str | None
    best: str | None
    best_time: str | None
    price_level: int | None
    user_id: int
    user: UserResponse
    images: list[ImageResponse]
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class SpotsResponse(BaseModel):
    items: list[SpotResponse]
    total: int
    page: int
    size: int
    pages: int
