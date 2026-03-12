import asyncio
import sys
import os

# Import individual seed modules
# Note: Some are in scripts/ folder
import seed
import seed_customers
import seed_products
import seed_party_menus
import seed_delivery_areas

# For scripts/seed_categories.py, we'll need a different approach since it's in a subfolder
sys.path.append(os.path.join(os.getcwd(), 'scripts'))
import seed_categories

async def run_all_seeds():
    print("🚀 Starting Master Seed Process...")
    
    print("\n--- Seeding Categories ---")
    await seed_categories.seed_categories()
    
    print("\n--- Seeding Products ---")
    await seed_products.main()
    
    print("\n--- Seeding Party Menus ---")
    await seed_party_menus.main()
    
    print("\n--- Seeding Admin and Initial Customers ---")
    await seed.main()
    
    print("\n--- Seeding 50 More Customers ---")
    await seed_customers.main()
    
    print("\n--- Seeding Delivery Areas ---")
    await seed_delivery_areas.main()
    
    print("\n✅ All seeding processes completed successfully!")

if __name__ == "__main__":
    asyncio.run(run_all_seeds())
