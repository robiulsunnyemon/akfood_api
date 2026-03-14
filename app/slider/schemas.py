from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SliderBase(BaseModel):
    image_url: str
    title: Optional[str] = None
    link_url: Optional[str] = None
    is_active: bool = True

class SliderCreate(SliderBase):
    pass

class SliderUpdate(BaseModel):
    image_url: Optional[str] = None
    title: Optional[str] = None
    link_url: Optional[str] = None
    is_active: Optional[bool] = None

class SliderResponse(SliderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
