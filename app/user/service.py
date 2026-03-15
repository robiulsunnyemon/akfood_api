from fastapi import UploadFile, HTTPException, status
from app.db import db
from app.utils.cloudinary import upload_image
from .schemas import UserUpdateProfileRequest

async def update_user_profile(user_id: int, update_data: UserUpdateProfileRequest):
    """
    Updates user info. Splits the single 'name' field into first_name and last_name.
    """
    # Simple split for the name wireframe (Mirable Lily -> Mirable, Lily)
    name_parts = update_data.name.strip().split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    # Check if new email is already taken by someone else
    existing_user = await db.user.find_first(
        where={
            "email": update_data.email,
            "id": {"not": user_id}
        }
    )
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use by another account.")

    # Check if phone number is taken by someone else
    existing_phone = await db.user.find_first(
        where={
            "phone_number": update_data.phone_number,
            "id": {"not": user_id}
        }
    )
    if existing_phone:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number is already in use by another account.")

    updated_user = await db.user.update(
        where={"id": user_id},
        data={
            "first_name": first_name,
            "last_name": last_name,
            "email": update_data.email,
            "phone_number": update_data.phone_number,
            "district": update_data.district,
            "city": update_data.city,
            "address": update_data.address
        }
    )
    
    # Add notification
    await db.notification.create(
        data={
            "user_id": user_id,
            "title": "Profile Updated",
            "message": "Your profile information has been successfully updated.",
            "type": "PROFILE"
        }
    )
    
    return updated_user

async def update_profile_image(user_id: int, file: UploadFile):
    """
    Uploads the provided file to Cloudinary and updates the user's profile_img_url
    """
    secure_url = await upload_image(file)
    
    updated_user = await db.user.update(
        where={"id": user_id},
        data={"profile_img_url": secure_url}
    )
    
    # Add notification
    await db.notification.create(
        data={
            "user_id": user_id,
            "title": "Profile Picture Updated",
            "message": "Your profile picture has been successfully updated.",
            "type": "PROFILE"
        }
    )
    
    return updated_user

async def get_customers(skip: int = 0, take: int = 20):
    """
    Fetches all users with the CUSTOMER role with pagination.
    """
    total = await db.user.count(where={"role": "CUSTOMER"})
    items = await db.user.find_many(
        where={"role": "CUSTOMER"},
        skip=skip,
        take=take,
        order={"created_at": "desc"}
    )
    return {"items": items, "total": total}
