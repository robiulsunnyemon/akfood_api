from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    image_url: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None

class CategoryRead(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
