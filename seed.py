import asyncio
import bcrypt
from prisma import Prisma

async def main():
    db = Prisma()
    await db.connect()

    try:
        # Generate hash for default password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw("password123".encode('utf-8'), salt).decode('utf-8')

        # Create 1 ADMIN
        admin_data = {
            "first_name": "Super",
            "last_name": "Admin",
            "email": "admin@example.com",
            "phone_number": "00000000000",
            "district": "Dhaka",
            "city": "Mega City",
            "address": "123 Admin Lane",
            "hashed_password": hashed_password,
            "role": "ADMIN"
        }
        
        # Check if exists first to make it safe to re-run
        exists = await db.user.find_unique(where={"email": admin_data["email"]})
        if not exists:
            await db.user.create(data=admin_data)
            print("ADMIN created.")

        # Create 5 CUSTOMERs
        for i in range(1, 6):
            customer_data = {
                "first_name": "Customer",
                "last_name": f"{i}",
                "email": f"customer{i}@example.com",
                "phone_number": f"0170000000{i}",
                "district": "Dhaka",
                "city": "Test City",
                "address": f"Customer Area {i}",
                "hashed_password": hashed_password,
                "role": "CUSTOMER"
            }
            exists = await db.user.find_unique(where={"email": customer_data["email"]})
            if not exists:
                await db.user.create(data=customer_data)
                print(f"CUSTOMER {customer_data['email']} created.")

        print("Seeding completed successfully!")
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
