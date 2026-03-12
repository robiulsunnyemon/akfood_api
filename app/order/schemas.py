from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class OrderItemCreate(BaseModel):
    product_id: Optional[int] = None
    variation_id: Optional[int] = None
    party_menu_id: Optional[int] = None
    quantity: int

class OrderCreate(BaseModel):
    city: str
    location: str
    address: str
    special_instruction: Optional[str] = None
    phone_number: str
    payment_method: str

class OrderItemResponse(BaseModel):
    id: int
    product_id: Optional[int] = None
    variation_id: Optional[int] = None
    party_menu_id: Optional[int] = None
    name: str
    price: float
    image_url: Optional[str] = None
    quantity: int

    class Config:
        from_attributes = True

class UserShortResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True

from app.review.schemas import ReviewResponse

class OrderResponse(BaseModel):
    id: int
    user_id: int
    user: Optional[UserShortResponse] = None
    city: str
    location: str
    address: str
    special_instruction: Optional[str] = None
    phone_number: Optional[str] = None
    payment_method: str
    subtotal: float
    delivery_fee: float
    total: float
    status: OrderStatus
    payment_status: PaymentStatus
    transaction_id: Optional[str] = None
    items: List[OrderItemResponse]
    review: Optional[ReviewResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
