from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductVariationBase(BaseModel):
    name: str
    price: float

class ProductVariationCreate(ProductVariationBase):
    pass

class ProductVariationRead(ProductVariationBase):
    id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int

class ProductCreate(ProductBase):
    image_url: Optional[str] = None
    variations: List[ProductVariationCreate]

class ProductVariationUpdate(BaseModel):
    id: Optional[int] = None
    name: str
    price: float

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    variations: Optional[List[ProductVariationUpdate]] = None

class ProductRead(ProductBase):
    id: int
    image_url: Optional[str] = None
    variations: List[ProductVariationRead]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedProductResponse(BaseModel):
    items: List[ProductRead]
    total: int
    page: int
    size: int
