from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.product.schemas import ProductRead

class PartyMenuItemResponse(BaseModel):
    id: int
    party_menu_id: int
    product_id: int
    product: ProductRead
    created_at: datetime

class PartyMenuBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: float
    category: Optional[str] = None

class PartyMenuCreate(PartyMenuBase):
    product_ids: List[int]

class PartyMenuUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    product_ids: Optional[List[int]] = None

class PartyMenuResponse(PartyMenuBase):
    id: int
    items: List[PartyMenuItemResponse]
    created_at: datetime
    updated_at: datetime

class PartyMenuPaginatedResponse(BaseModel):
    items: List[PartyMenuResponse]
    total: int
