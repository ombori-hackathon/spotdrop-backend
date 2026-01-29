from datetime import datetime

from pydantic import BaseModel


class ImageCreate(BaseModel):
    is_primary: bool = False


class ImageResponse(BaseModel):
    id: int
    url: str
    is_primary: bool
    spot_id: int
    created_at: datetime

    class Config:
        from_attributes = True
