from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.product.schemas import ProductRead, ProductVariationRead
from app.party_menu.schemas import PartyMenuResponse

class CartItemCreate(BaseModel):
    product_id: Optional[int] = None
    variation_id: Optional[int] = None
    party_menu_id: Optional[int] = None
    quantity: int = 1

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: Optional[int] = None
    product: Optional[ProductRead] = None
    variation_id: Optional[int] = None
    variation: Optional[ProductVariationRead] = None
    party_menu_id: Optional[int] = None
    party_menu: Optional[PartyMenuResponse] = None
    quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    subtotal: float
    shipping: float = 0.0
    total: float
