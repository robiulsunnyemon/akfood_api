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
