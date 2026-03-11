from pydantic import BaseModel
from typing import List

class DeliveryAreaBase(BaseModel):
    city: str
    locations: List[str]

class DeliveryAreaCreate(DeliveryAreaBase):
    pass

class DeliveryAreaResponse(DeliveryAreaBase):
    id: int

    class Config:
        from_attributes = True
