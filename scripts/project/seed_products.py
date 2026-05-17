import asyncio
from prisma import Prisma

async def main():
    db = Prisma()
    await db.connect()

    try:
        # Get existing categories or create a default one
        categories = await db.category.find_many()
        if not categories:
            print("No categories found. Creating a default 'General' category.")
            default_category = await db.category.create(
                data={
                    "name": "General",
                    "image_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0"
                }
            )
            cat_id = default_category.id
        else:
            cat_id = categories[0].id

        print("Starting to seed 10 products...")

        products_data = [
            {
                "name": "Classic Cheeseburger",
                "description": "Juicy beef patty with melted cheese, lettuce, and our special sauce.",
                "image_url": "https://pixabay.com/images/download/x-1552436_1920.jpg",
                "is_active": True,
            },
            {
                "name": "Margherita Pizza",
                "description": "Classic Italian pizza with fresh tomatoes, mozzarella, and basil.",
                "image_url": "https://pixabay.com/images/download/x-8711272_1920.jpg",
                "is_active": True,
            },
            {
                "name": "Spicy Chicken Wings",
                "description": "Crispy fried wings tossed in our signature spicy buffalo sauce.",
                "image_url": "https://pixabay.com/images/download/x-8547127_1920.jpg",
                "is_active": True,
            },
            {
                "name": "Caesar Salad",
                "description": "Fresh romaine lettuce, croutons, parmesan cheese, and creamy caesar dressing.",
                "image_url": "https://pixabay.com/images/download/x-246818_1920.jpg",
                "is_active": True,
            },
            {
                "name": "Chocolate Brownie",
                "description": "Rich and fudgy chocolate brownie topped with vanilla ice cream.",
                "image_url": "https://pixabay.com/images/download/x-1133146_1920.jpg",
                "is_active": True,
            },
            {
                "name": "French Fries",
                "description": "Crispy golden french fries served with ketchup.",
                "image_url": "https://pixabay.com/images/download/x-2167281_1920.jpg",
                "is_active": True,
            },
            {
                "name": "Pasta Carbonara",
                "description": "Creamy pasta with bacon, parmesan, and black pepper.",
                "image_url": "https://pixabay.com/images/download/x-2059852_1920.jpg",
                "is_active": True,
            },
            {
                "name": "Grilled Steak",
                "description": "Perfectly grilled beef steak with a side of mashed potatoes.",
                "image_url": "https://pixabay.com/images/download/x-2169305_1920.jpg",
                "is_active": True,
            },
            {
                "name": "Sushi Platter",
                "description": "Assorted fresh sushi rolls with soy sauce and wasabi.",
                "image_url": "https://pixabay.com/images/download/x-1618622_1920.jpg",
                "is_active": True,
            },
            {
                "name": "Strawberry Cheesecake",
                "description": "Creamy cheesecake topped with fresh strawberry compote.",
                "image_url": "https://pixabay.com/images/download/x-4371777_1920.jpg",
                "is_active": True,
            }
        ]

        for i, data in enumerate(products_data):
            try:
                # Add category connection
                data["category"] = {"connect": {"id": cat_id}}
                
                # Add some variations
                data["variations"] = {
                    "create": [
                        {"name": "Regular", "price": 150.0},
                        {"name": "Large", "price": 250.0}
                    ]
                }

                await db.product.create(data=data)
                print(f"Product {i+1}: '{data['name']}' created successfully.")
            except Exception as e:
                print(f"Failed to create product '{data['name']}': {e}")

        print("\nSeeding of 10 products completed!")

    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
