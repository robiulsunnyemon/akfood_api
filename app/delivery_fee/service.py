from prisma import Prisma
from typing import List, Optional

db = Prisma()

async def create_delivery_fee(data: dict) -> dict:
    if not db.is_connected():
        await db.connect()
    
    # Check if a fee already exists
    existing = await db.deliveryfee.find_first()
    if existing:
        # Update the existing one instead of creating a new one
        updated = await db.deliveryfee.update(where={"id": existing.id}, data=data)
        return updated.model_dump()
        
    delivery_fee = await db.deliveryfee.create(data=data)
    return delivery_fee.model_dump()

async def get_all_delivery_fees() -> List[dict]:
    if not db.is_connected():
        await db.connect()
    fees = await db.deliveryfee.find_many()
    return [fee.model_dump() for fee in fees]

async def get_delivery_fee_by_id(fee_id: int) -> Optional[dict]:
    if not db.is_connected():
        await db.connect()
    fee = await db.deliveryfee.find_unique(where={"id": fee_id})
    return fee.model_dump() if fee else None

async def update_delivery_fee(fee_id: int, data: dict) -> Optional[dict]:
    if not db.is_connected():
        await db.connect()
    updated = await db.deliveryfee.update(where={"id": fee_id}, data=data)
    return updated.model_dump() if updated else None

async def delete_delivery_fee(fee_id: int) -> bool:
    if not db.is_connected():
        await db.connect()
    deleted = await db.deliveryfee.delete(where={"id": fee_id})
    return deleted is not None
