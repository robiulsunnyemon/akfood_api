import asyncio
from app.db import db
from app.dashboard.service import get_dashboard_stats

async def test_dashboard():
    await db.connect()
    
    print("\nExecuting get_dashboard_stats(week)...")
    try:
        stats = await get_dashboard_stats("week")
        print("\n--- Dashboard Stats (Week) ---")
        print(f"Active Listings: {stats['active_listings']}")
        print(f"Active Menus: {stats['active_menus']}")
        print(f"Pending Orders: {stats['pending_orders']}")
        print(f"Total Revenue: {stats['total_revenue']}")
        print(f"Revenue Chart Data points: {len(stats['revenue_chart'])}")
        print(f"User Growth Chart Data points: {len(stats['user_growth_chart'])}")
    except Exception as e:
        print(f"Failed: {e}")

    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(test_dashboard())
