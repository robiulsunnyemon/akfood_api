from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..auth.service import get_current_user
from ..auth.schemas import UserRead
from . import schemas
from .service import ProductSectionService

router = APIRouter(prefix="/product-sections", tags=["Product Sections"])
service = ProductSectionService()

@router.get("/home", response_model=List[schemas.HomeSectionResponse])
async def get_home_sections():
    return await service.get_home_sections()

@router.get("/", response_model=List[schemas.ProductSectionRead])
async def get_all_sections(current_user: UserRead = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return await service.get_all_sections()

@router.post("/", response_model=schemas.ProductSectionRead)
async def create_section(data: schemas.ProductSectionCreate, current_user: UserRead = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return await service.create_section(data)

@router.put("/{section_id}", response_model=schemas.ProductSectionRead)
async def update_section(section_id: int, data: schemas.ProductSectionUpdate, current_user: UserRead = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return await service.update_section(section_id, data)

@router.delete("/{section_id}")
async def delete_section(section_id: int, current_user: UserRead = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return await service.delete_section(section_id)

@router.post("/{section_id}/assign/{product_id}")
async def assign_product(section_id: int, product_id: int, order_index: int = 0, current_user: UserRead = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return await service.assign_product_to_section(section_id, product_id, order_index)

@router.delete("/{section_id}/remove/{product_id}")
async def remove_product(section_id: int, product_id: int, current_user: UserRead = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return await service.remove_product_from_section(section_id, product_id)
