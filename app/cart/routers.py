from fastapi import APIRouter, Depends, status, HTTPException
from app.auth.service import get_current_user
from . import schemas, service
from typing import List, Optional

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

@router.get("", response_model=schemas.CartResponse)
async def get_cart(current_user = Depends(get_current_user)):
    """Get the current user's cart"""
    return await service.get_user_cart(current_user.id)

@router.post("", response_model=schemas.CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(data: schemas.CartItemCreate, current_user = Depends(get_current_user)):
    """Add an item to the cart"""
    return await service.add_to_cart(current_user.id, data)

@router.put("/{id}", response_model=Optional[schemas.CartItemResponse])
async def update_cart_item(id: int, data: schemas.CartItemUpdate, current_user = Depends(get_current_user)):
    """Update cart item quantity"""
    return await service.update_cart_item(id, current_user.id, data.quantity)

@router.delete("/{id}")
async def delete_cart_item(id: int, current_user = Depends(get_current_user)):
    """Remove an item from the cart"""
    return await service.delete_cart_item(id, current_user.id)
