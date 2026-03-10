from fastapi import APIRouter, Depends, UploadFile, File
from app.auth.service import get_current_user, get_admin_user
from . import schemas, service
from typing import List

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(current_user = Depends(get_current_user)):
    """Get the currently authenticated user's profile info"""
    return current_user

@router.get("/customers", response_model=schemas.UserListResponse)
async def get_all_customers(
    page: int = 1, 
    size: int = 20, 
    current_admin = Depends(get_admin_user)
):
    """
    Get all users with the CUSTOMER role with pagination.
    Only accessible by ADMIN users.
    """
    skip = (page - 1) * size
    customers = await service.get_customers(skip=skip, take=size)
    return customers

@router.put("/profile", response_model=schemas.UserResponse)
async def update_my_profile(
    update_data: schemas.UserUpdateProfileRequest, 
    current_user = Depends(get_current_user)
):
    """Updates textual profile properties based on the wireframe screen"""
    updated_user = await service.update_user_profile(user_id=current_user.id, update_data=update_data)
    return updated_user

@router.put("/profile-image", response_model=schemas.UserResponse)
async def update_my_profile_image(
    file: UploadFile = File(...), 
    current_user = Depends(get_current_user)
):
    """
    Uploads and updates the user's profile picture. 
    Requires CLOUDINARY credentials in the .env file.
    """
    updated_user = await service.update_profile_image(user_id=current_user.id, file=file)
    return updated_user
