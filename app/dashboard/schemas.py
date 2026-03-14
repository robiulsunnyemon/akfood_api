from pydantic import BaseModel
from typing import List

class StatPoint(BaseModel):
    label: str
    value: float

class DashboardStatsResponse(BaseModel):
    active_listings: int
    active_menus: int
    pending_orders: int
    total_revenue: float
    revenue_chart: List[StatPoint]
    user_growth_chart: List[StatPoint]
