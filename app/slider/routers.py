from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from app.auth.service import get_current_user, get_admin_user
from app.db import get_db
from prisma import Prisma
from . import service, schemas
from app.utils.cloudinary import upload_image

router = APIRouter(prefix="/sliders", tags=["Sliders"])

@router.post("/", response_model=schemas.SliderResponse)
async def create_new_slider(
    title: Optional[str] = Form(None),
    link_url: Optional[str] = Form(None),
    image: UploadFile = File(...),
    db: Prisma = Depends(get_db),
    admin = Depends(get_admin_user)
):
    # Upload image to Cloudinary
    image_url = await upload_image(image, folder="akfood/sliders")
    
    data = schemas.SliderCreate(
        image_url=image_url,
        title=title,
        link_url=link_url,
        is_active=True
    )
    return await service.create_slider(db, data)

@router.get("/", response_model=List[schemas.SliderResponse])
async def get_sliders(
    active_only: bool = False,
    db: Prisma = Depends(get_db)
):
    return await service.get_all_sliders(db, active_only)

@router.put("/{slider_id}", response_model=schemas.SliderResponse)
async def update_slider_info(
    slider_id: int,
    data: schemas.SliderUpdate,
    db: Prisma = Depends(get_db),
    admin = Depends(get_admin_user)
):
    slider = await service.get_slider_by_id(db, slider_id)
    if not slider:
        raise HTTPException(status_code=404, detail="Slider not found")
        
    return await service.update_slider(db, slider_id, data)

@router.delete("/{slider_id}")
async def remove_slider(
    slider_id: int,
    db: Prisma = Depends(get_db),
    admin = Depends(get_admin_user)
):
    slider = await service.get_slider_by_id(db, slider_id)
    if not slider:
        raise HTTPException(status_code=404, detail="Slider not found")
        
    await service.delete_slider(db, slider_id)
    return {"message": "Slider deleted successfully"}
