from fastapi import APIRouter, Depends, status
from app.auth.service import get_admin_user
from . import schemas, service
from typing import List

router = APIRouter(
    prefix="/party-menu",
    tags=["Party Menu"]
)

@router.get("", response_model=schemas.PartyMenuPaginatedResponse)
async def get_all_party_menus(page: int = 1, size: int = 21):
    """Get all party menus with pagination"""
    skip = (page - 1) * size
    return await service.get_all_party_menus(skip=skip, take=size)

@router.get("/{id}", response_model=schemas.PartyMenuResponse)
async def get_party_menu(id: int):
    """Get a specific party menu by ID"""
    return await service.get_party_menu_by_id(id)

@router.post("", response_model=schemas.PartyMenuResponse, status_code=status.HTTP_201_CREATED)
async def create_party_menu(data: schemas.PartyMenuCreate, admin = Depends(get_admin_user)):
    """Create a new party menu (Admin only)"""
    return await service.create_party_menu(data)

@router.put("/{id}", response_model=schemas.PartyMenuResponse)
async def update_party_menu(id: int, data: schemas.PartyMenuUpdate, admin = Depends(get_admin_user)):
    """Update a party menu (Admin only)"""
    return await service.update_party_menu(id, data)

@router.delete("/{id}")
async def delete_party_menu(id: int, admin = Depends(get_admin_user)):
    """Delete a party menu (Admin only)"""
    return await service.delete_party_menu(id)
