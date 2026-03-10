import asyncio
import sys
import os

# Add the project root to sys.path to allow importing from 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import db

async def seed_categories():
    categories = [
        "Appetizer", "Broast/Juicy Chicken", "Burger", "Sea Food", 
        "Ala Cart/Continental", "Rice Bowl", "Platter", "Salad", 
        "Pasta", "Soup", "Sandwich", "Add On", "French Fries", 
        "Dessert", "Soft Drinks"
    ]
    
    print(f"Connecting to database...")
    await db.connect()
    
    print(f"Seeding {len(categories)} categories...")
    
    for cat_name in categories:
        # Check if exists
        existing = await db.category.find_unique(where={"name": cat_name})
        if not existing:
            await db.category.create(data={"name": cat_name})
            print(f"Created category: {cat_name}")
        else:
            print(f"Category already exists: {cat_name}")
            
    await db.disconnect()
    print("Seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_categories())
