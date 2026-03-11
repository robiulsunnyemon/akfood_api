from app.db import db
from prisma.models import DeliveryArea
from typing import List

async def create_delivery_area(data: dict) -> DeliveryArea:
    return await db.deliveryarea.create(data=data)

async def get_all_delivery_areas() -> List[DeliveryArea]:
    return await db.deliveryarea.find_many()

async def get_delivery_area_by_id(area_id: int) -> DeliveryArea | None:
    return await db.deliveryarea.find_unique(where={"id": area_id})

async def get_delivery_area_by_city(city: str) -> DeliveryArea | None:
    return await db.deliveryarea.find_unique(where={"city": city})

async def update_delivery_area(area_id: int, data: dict) -> DeliveryArea | None:
    return await db.deliveryarea.update(where={"id": area_id}, data=data)

async def delete_delivery_area(area_id: int) -> DeliveryArea | None:
    return await db.deliveryarea.delete(where={"id": area_id})
