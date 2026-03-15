from fastapi import APIRouter, Depends
from . import schemas, service
from app.auth.service import get_admin_user

router = APIRouter(prefix="/cms", tags=["CMS (Static Pages)"])

@router.get("/{slug}", response_model=schemas.CmsPageRead)
async def get_page(slug: str):
    """Fetch content of a static page (About Us, etc.)"""
    return await service.get_page_by_slug(slug)

@router.put("/{slug}", response_model=schemas.CmsPageRead)
async def update_page(slug: str, data: schemas.CmsPageUpdate, admin = Depends(get_admin_user)):
    """Update content of a static page (Admin Only)"""
    return await service.update_page_content(slug, data)
