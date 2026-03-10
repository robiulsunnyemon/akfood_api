import asyncio
import random
from prisma import Prisma

async def main():
    db = Prisma()
    await db.connect()

    try:
        # Get existing categories
        categories = await db.category.find_many()
        if not categories:
            print("No categories found. Please seed categories first.")
            return
        
        category_ids = [c.id for c in categories]
        
        # Real food images from Unsplash
        image_pool = [
            "https://images.unsplash.com/photo-1567620905732-2d1ec7bb7445?auto=format&fit=crop&w=800&q=80", # Pancakes
            "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80", # Salad
            "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=800&q=80", # Pizza
            "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80", # Pizza 2
            "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=800&q=80", # Grilled Meat
            "https://images.unsplash.com/photo-1565958011703-44f9829ba187?auto=format&fit=crop&w=800&q=80", # Cake
            "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?auto=format&fit=crop&w=800&q=80", # Sushi
            "https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=800&q=80", # Salmon
            "https://images.unsplash.com/photo-1473093226795-af9932fe5856?auto=format&fit=crop&w=800&q=80", # Pasta
            "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=800&q=80", # Salad 2
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80", # Steak
            "https://images.unsplash.com/photo-1493770348161-369560ae357d?auto=format&fit=crop&w=800&q=80", # Breakfast
            "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a?auto=format&fit=crop&w=800&q=80", # Soup
            "https://images.unsplash.com/photo-1484723088339-599cb551ee09?auto=format&fit=crop&w=800&q=80", # Toast
            "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=800&q=80", # Vegetables
            "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=800&q=80", # Fine Dining
            "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80", # Salad Bowl
            "https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?auto=format&fit=crop&w=800&q=80", # Burger
            "https://images.unsplash.com/photo-1529006557870-17483443a28f?auto=format&fit=crop&w=800&q=80", # Fries
            "https://images.unsplash.com/photo-1506084868730-342b23639160?auto=format&fit=crop&w=800&q=80", # Healthy Breakfast
        ]

        food_names = [
            "Cheese Blast Burger", "Grilled Chicken Platter", "Spicy Pepperoni Pizza", 
            "Creamy Alfredo Pasta", "Hydrabadi Mutton Biryani", "Crispy Fish & Chips",
            "Avocado Toast Supreme", "Classic Caesar Salad", "Teriyaki Salmon Bowl",
            "Mushroom Swiss Burger", "Fettuccine Carbonara", "Steak Diane", "Lobster Thermidor",
            "Chicken Tikka Masala", "Beef Bulgogi", "Pad Thai Noodles", "Dim Sum Basket",
            "Margherita Pizza Pizza", "Tandoori Platter", "Chocolate Lava Cake"
        ]

        descriptions = [
            "Juicy beef patty with melted cheese, fresh veggies, and special sauce.",
            "Perfectly grilled chicken served with seasonal vegetables and mash.",
            "Thin crust topped with premium pepperoni and mozzarella cheese.",
            "Classic Italian pasta with rich cream and parmesan cheese.",
            "Aromatic rice cooked with tender mutton and authentic spices."
        ]

        for i in range(30):
            name = random.choice(food_names) + f" {i+1}"
            desc = random.choice(descriptions)
            img = random.choice(image_pool)
            cat_id = random.choice(category_ids)
            
            # Create product
            product = await db.product.create(
                data={
                    "name": name,
                    "description": desc,
                    "image_url": img,
                    "category_id": cat_id,
                    "variations": {
                        "create": [
                            {"name": "For 1 person", "price": random.randint(10, 50)},
                            {"name": "For 2 persons", "price": random.randint(40, 90)},
                            {"name": "For 3 persons", "price": random.randint(60, 130)},
                            {"name": "For 5 persons", "price": random.randint(100, 250)},
                        ]
                    }
                }
            )
            print(f"Product {i+1}: {name} created with category ID {cat_id}")

        print("\nSeeding of 30 products completed successfully!")
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
