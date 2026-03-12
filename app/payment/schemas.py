from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PaymentStats(BaseModel):
    platform_earnings: float
    total_revenue: float
    ssl_cost: float

class TransactionResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    transaction_id: str
    status: str
    created_at: datetime
    customer_name: str

class PaymentSessionCreate(BaseModel):
    order_id: int
