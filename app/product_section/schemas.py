from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..product.schemas import ProductRead

class SectionProductBase(BaseModel):
    product_id: int
    order_index: int = 0

class SectionProductCreate(SectionProductBase):
    pass

class SectionProductRead(SectionProductBase):
    id: int
    product: ProductRead

    class Config:
        from_attributes = True

class ProductSectionBase(BaseModel):
    name: str
    order_index: int = 0
    is_active: bool = True

class ProductSectionCreate(ProductSectionBase):
    pass

class ProductSectionUpdate(BaseModel):
    name: Optional[str] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None

class ProductSectionRead(ProductSectionBase):
    id: int
    products: Optional[List[SectionProductRead]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class HomeSectionResponse(BaseModel):
    id: int
    name: str
    products: List[ProductRead]
