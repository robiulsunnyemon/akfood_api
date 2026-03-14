from fastapi import APIRouter, Depends, Query
from app.auth.service import get_admin_user
from . import schemas, service

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/stats", response_model=schemas.DashboardStatsResponse)
async def get_dashboard_statistics(
    period: str = Query("week", description="Filter period: week, month, year"),
    admin=Depends(get_admin_user)
):
    """
    Get all dashboard statistics (Admin only).
    """
    return await service.get_dashboard_stats(period)
