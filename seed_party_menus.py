import asyncio
import random
from prisma import Prisma

async def main():
    db = Prisma()
    await db.connect()

    # Fetch existing products to use in menus
    products = await db.product.find_many()
    if not products:
        print("No products found in database. Please seed products first.")
        await db.disconnect()
        return

    product_ids = [p.id for p in products]

    menu_titles = [
        "Corporate Lunch Box", "Wedding Feast", "Birthday Bonanza", 
        "Family Gathering Platter", "Office Party Special", "Evening Snacks Combo",
        "Classic Buffet", "Royal Dastarkhawan", "Mega Meal Deal", 
        "Executive Breakfast", "Student Savings Box", "Weekend Treat"
    ]
    
    categories = ["Premium", "Standard", "Budget", "Special", "Festive"]
    
    # Random realistic images for menus
    image_urls = [
        "https://images.unsplash.com/photo-1555243629-7eb23b0ed580",
        "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe",
        "https://images.unsplash.com/photo-1567620905732-2d1ec7bb7445",
        "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38",
        "https://images.unsplash.com/photo-1482049016688-2d3e1b311543",
        "https://images.unsplash.com/photo-1467003909585-2f8a72700288",
        "https://images.unsplash.com/photo-1473093226795-af9932fe5856",
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836"
    ]

    print(f"Starting to seed 51 party menus with {len(products)} available products...")

    for i in range(51):
        title = f"{random.choice(menu_titles)} #{i+1}"
        description = f"Specially curated {title.lower()} featuring a delightful selection of our best items."
        price = round(random.uniform(500, 5000), 2)
        category = random.choice(categories)
        image_url = random.choice(image_urls)
        
        # Select 2 to 5 random products for this menu
        num_items = random.randint(2, 5)
        selected_pids = random.sample(product_ids, min(num_items, len(product_ids)))

        try:
            await db.partymenu.create(
                data={
                    "title": title,
                    "description": description,
                    "price": price,
                    "category": category,
                    "image_url": image_url,
                    "items": {
                        "create": [{"product_id": pid} for pid in selected_pids]
                    }
                }
            )
            print(f"Party Menu {i+1}: '{title}' created with {len(selected_pids)} items.")
        except Exception as e:
            print(f"Failed to create party menu {i+1}: {e}")

    await db.disconnect()
    print("\nSeeding of 51 party menus completed!")

if __name__ == "__main__":
    asyncio.run(main())
