import asyncio
from prisma import Prisma

async def reset_database():
    print("⚠️  WARNING: You are about to DELETE ALL DATA from the database. ⚠️")
    confirm = input("Are you sure you want to proceed? Type 'YES' to confirm: ")
    
    if confirm != 'YES':
        print("Database reset cancelled.")
        return

    db = Prisma()
    await db.connect()
    print("\nConnecting to database...")

    try:
        print("Clearing all tables...")
        
        # Delete models in order of dependencies (child tables first, then parent tables)
        
        print("- Deleting Cart Items...")
        await db.cartitem.delete_many()
        
        print("- Deleting Order Items...")
        await db.orderitem.delete_many()
        
        print("- Deleting Reviews...")
        await db.review.delete_many()
        
        print("- Deleting Orders...")
        await db.order.delete_many()
        
        print("- Deleting OTPs...")
        await db.otp.delete_many()
        
        print("- Deleting Party Menu Items...")
        await db.partymenuitem.delete_many()
        
        print("- Deleting Party Menus...")
        await db.partymenu.delete_many()
        
        print("- Deleting Product Variations...")
        await db.productvariation.delete_many()
        
        print("- Deleting Products...")
        await db.product.delete_many()
        
        print("- Deleting Categories...")
        await db.category.delete_many()
        
        print("- Deleting Delivery Areas...")
        await db.deliveryarea.delete_many()
        
        print("- Deleting Delivery Fees...")
        await db.deliveryfee.delete_many()
        
        print("- Deleting Users...")
        await db.user.delete_many()

        print("\n✅ Database has been successfully cleared and reset!")
        print("You can now run seeds again.")
        
    except Exception as e:
        print(f"\n❌ An error occurred while resetting the database: {e}")
    finally:
        await db.disconnect()
        print("Database connection closed.")

if __name__ == "__main__":
    asyncio.run(reset_database())
