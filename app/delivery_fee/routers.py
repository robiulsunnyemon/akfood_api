from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.delivery_fee import service
from app.delivery_fee.schemas import DeliveryFeeCreate, DeliveryFeeResponse
from app.auth.service import get_current_user
from prisma.models import User
from prisma.enums import Role

router = APIRouter(prefix="/delivery-fee", tags=["Delivery Fee"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@router.post("/", response_model=DeliveryFeeResponse)
async def create_delivery_fee(
    fee_data: DeliveryFeeCreate,
    current_user: User = Depends(require_admin)
):
    # Only allow one fee ideally, but let's just create it
    return await service.create_delivery_fee(fee_data.model_dump())

@router.get("/", response_model=List[DeliveryFeeResponse])
async def get_delivery_fees():
    return await service.get_all_delivery_fees()

@router.get("/{fee_id}", response_model=DeliveryFeeResponse)
async def get_delivery_fee(fee_id: int):
    fee = await service.get_delivery_fee_by_id(fee_id)
    if not fee:
        raise HTTPException(status_code=404, detail="Delivery fee not found")
    return fee

@router.put("/{fee_id}", response_model=DeliveryFeeResponse)
async def update_delivery_fee(
    fee_id: int,
    fee_data: DeliveryFeeCreate,
    current_user: User = Depends(require_admin)
):
    updated = await service.update_delivery_fee(fee_id, fee_data.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Delivery fee not found")
    return updated

@router.delete("/{fee_id}")
async def delete_delivery_fee(
    fee_id: int,
    current_user: User = Depends(require_admin)
):
    deleted = await service.delete_delivery_fee(fee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Delivery fee not found")
    return {"message": "Delivery fee deleted successfully"}
