from app.db import db
from datetime import datetime, timedelta
from typing import Dict, Any

async def get_dashboard_stats(period: str = "week") -> Dict[str, Any]:
    # 1. Active Listings (Products where is_active is true)
    # If is_active doesn't exist on all your users' DBs yet, handle gracefully.
    try:
        active_listings = await db.product.count(where={"is_active": True})
    except Exception:
        # Fallback if is_active is not migrated yet
        active_listings = await db.product.count()

    # 2. Active Menus
    active_menus = await db.partymenu.count()

    # 3. Pending Orders
    pending_orders = await db.order.count(where={"status": "PENDING"})

    # 4. Total Revenue (Delivered orders or Paid orders)
    # We will sum the "total" field of delivered orders
    delivered_orders = await db.order.find_many(where={"status": "DELIVERED"})
    total_revenue = sum(order.total for order in delivered_orders)

    # 5. Charts Data calculation based on period
    now = datetime.now()
    revenue_chart = []
    user_growth_chart = []

    if period == "week":
        # Last 7 days
        for i in range(6, -1, -1):
            date = now - timedelta(days=i)
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            # Revenue for the day
            daily_orders = await db.order.find_many(where={
                "status": "DELIVERED",
                "created_at": {"gte": start_of_day, "lte": end_of_day}
            })
            daily_revenue = sum(o.total for o in daily_orders)
            revenue_chart.append({"label": date.strftime("%a"), "value": daily_revenue})

            # Users for the day
            daily_users = await db.user.count(where={
                "created_at": {"gte": start_of_day, "lte": end_of_day}
            })
            user_growth_chart.append({"label": date.strftime("%a"), "value": daily_users})

    elif period == "month":
        # Last 4 weeks loosely
        for i in range(4, 0, -1):
            # This is a simplified weekly grouping
            start_date = now - timedelta(days=i*7)
            end_date = start_date + timedelta(days=6)
            
            label = f"W{5-i}"
            
            weekly_orders = await db.order.find_many(where={
                "status": "DELIVERED",
                "created_at": {"gte": start_date, "lte": end_date}
            })
            revenue_chart.append({"label": label, "value": sum(o.total for o in weekly_orders)})
            
            weekly_users = await db.user.count(where={
                "created_at": {"gte": start_date, "lte": end_date}
            })
            user_growth_chart.append({"label": label, "value": weekly_users})
            
    elif period == "year":
        # Last 12 months
        for i in range(11, -1, -1):
            target_month = now.month - i
            target_year = now.year
            if target_month <= 0:
                target_month += 12
                target_year -= 1
                
            # naive start/end of month
            start_date = datetime(target_year, target_month, 1)
            # just up to the end of that month (roughly)
            if target_month == 12:
                end_date = datetime(target_year + 1, 1, 1) - timedelta(microseconds=1)
            else:
                end_date = datetime(target_year, target_month + 1, 1) - timedelta(microseconds=1)
                
            month_label = start_date.strftime("%b")
            
            monthly_orders = await db.order.find_many(where={
                "status": "DELIVERED",
                "created_at": {"gte": start_date, "lte": end_date}
            })
            revenue_chart.append({"label": month_label, "value": sum(o.total for o in monthly_orders)})
            
            monthly_users = await db.user.count(where={
                "created_at": {"gte": start_date, "lte": end_date}
            })
            user_growth_chart.append({"label": month_label, "value": monthly_users})

    return {
        "active_listings": active_listings,
        "active_menus": active_menus,
        "pending_orders": pending_orders,
        "total_revenue": total_revenue,
        "revenue_chart": revenue_chart,
        "user_growth_chart": user_growth_chart
    }
