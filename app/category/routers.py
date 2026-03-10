from fastapi import APIRouter, status, Depends
from . import schemas, service
from app.auth.service import get_admin_user
from typing import List

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("/", response_model=List[schemas.CategoryRead])
async def get_categories():
    """Get all food categories"""
    return await service.get_all_categories()

@router.post("/", response_model=schemas.CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(data: schemas.CategoryCreate, admin = Depends(get_admin_user)):
    """Create a new category (Admin only)"""
    return await service.create_category(data)

@router.put("/{id}", response_model=schemas.CategoryRead)
async def update_category(id: int, data: schemas.CategoryUpdate, admin = Depends(get_admin_user)):
    """Update a category (Admin only)"""
    return await service.update_category(id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: int, admin = Depends(get_admin_user)):
    """Delete a category (Admin only)"""
    await service.delete_category(id)
    return None
