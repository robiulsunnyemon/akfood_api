from fastapi import APIRouter, Depends
from prisma import Prisma
from app.db import get_db
from app.auth.service import get_current_user
from .schemas import ReviewCreate, ReviewResponse
from . import service
from prisma.models import User

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewResponse)
async def submit_review(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db)
):
    return await service.create_review(db, current_user.id, review_data)

