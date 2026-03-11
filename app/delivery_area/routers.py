from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.delivery_area import service
from app.delivery_area.schemas import DeliveryAreaCreate, DeliveryAreaResponse
from app.auth.service import get_current_user
from prisma.models import User
from prisma.enums import Role

router = APIRouter(prefix="/delivery-areas", tags=["Delivery Areas"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@router.post("/", response_model=DeliveryAreaResponse)
async def create_delivery_area(
    delivery_area: DeliveryAreaCreate,
    current_user: User = Depends(require_admin)
):
    existing_area = await service.get_delivery_area_by_city(delivery_area.city)
    if existing_area:
        raise HTTPException(status_code=400, detail="Delivery area for this city already exists")
    
    return await service.create_delivery_area(delivery_area.model_dump())

@router.get("/", response_model=List[DeliveryAreaResponse])
async def get_delivery_areas():
    return await service.get_all_delivery_areas()

@router.get("/{area_id}", response_model=DeliveryAreaResponse)
async def get_delivery_area(area_id: int):
    area = await service.get_delivery_area_by_id(area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Delivery area not found")
    return area

@router.put("/{area_id}", response_model=DeliveryAreaResponse)
async def update_delivery_area(
    area_id: int,
    delivery_area: DeliveryAreaCreate,
    current_user: User = Depends(require_admin)
):
    updated = await service.update_delivery_area(area_id, delivery_area.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Delivery area not found")
    return updated

@router.delete("/{area_id}")
async def delete_delivery_area(
    area_id: int,
    current_user: User = Depends(require_admin)
):
    deleted = await service.delete_delivery_area(area_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Delivery area not found")
    return {"message": "Delivery area deleted successfully"}
