from fastapi import APIRouter, status, Depends
from . import schemas, service
from app.auth.service import get_admin_user
from typing import List

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/", response_model=schemas.PaginatedProductResponse)
async def get_products(page: int = 1, size: int = 21, section_id: int = None):
    """Get foods with pagination"""
    skip = (page - 1) * size
    result = await service.get_all_products(skip=skip, take=size, section_id=section_id)
    return {
        "items": result["items"],
        "total": result["total"],
        "page": page,
        "size": size
    }

@router.post("/", response_model=schemas.ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(data: schemas.ProductCreate, admin = Depends(get_admin_user)):
    """Create a new product (Admin only)"""
    return await service.create_product(data)

@router.get("/{product_id}", response_model=schemas.ProductRead)
async def get_product(product_id: int):
    """Get a product by ID"""
    return await service.get_product_by_id(product_id)

@router.put("/{product_id}", response_model=schemas.ProductRead)
async def update_product(product_id: int, data: schemas.ProductUpdate, admin = Depends(get_admin_user)):
    """Update a product (Admin only)"""
    return await service.update_product(product_id, data)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, admin = Depends(get_admin_user)):
    """Delete a product (Admin only)"""
    return await service.delete_product(product_id)
