from pydantic import BaseModel

class DeliveryFeeCreate(BaseModel):
    fee: float

class DeliveryFeeResponse(BaseModel):
    id: int
    fee: float
