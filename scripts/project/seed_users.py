import asyncio
import bcrypt
from prisma import Prisma

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

async def main():
    db = Prisma()
    await db.connect()

    pw_hash = get_password_hash("123456")

    print("Starting to seed users...")

    users_data = [
        # 1 Admin
        {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@magpie.com",
            "phone_number": "+8801700000000",
            "district": "Dhaka",
            "city": "Uttara",
            "address": "123 Admin St",
            "hashed_password": pw_hash,
            "role": "ADMIN"
        },
        # 5 Customers
        {
            "first_name": "Customer",
            "last_name": "One",
            "email": "customer1@magpie.com",
            "phone_number": "+8801700000001",
            "district": "Dhaka",
            "city": "Gulshan",
            "address": "101 Customer Rd",
            "hashed_password": pw_hash,
            "role": "CUSTOMER"
        },
        {
            "first_name": "Customer",
            "last_name": "Two",
            "email": "customer2@magpie.com",
            "phone_number": "+8801700000002",
            "district": "Chattogram",
            "city": "Halishahar",
            "address": "202 Customer Rd",
            "hashed_password": pw_hash,
            "role": "CUSTOMER"
        },
        {
            "first_name": "Customer",
            "last_name": "Three",
            "email": "customer3@magpie.com",
            "phone_number": "+8801700000003",
            "district": "Sylhet",
            "city": "Zindabazar",
            "address": "303 Customer Rd",
            "hashed_password": pw_hash,
            "role": "CUSTOMER"
        },
        {
            "first_name": "Customer",
            "last_name": "Four",
            "email": "customer4@magpie.com",
            "phone_number": "+8801700000004",
            "district": "Rajshahi",
            "city": "Shaheb Bazar",
            "address": "404 Customer Rd",
            "hashed_password": pw_hash,
            "role": "CUSTOMER"
        },
        {
            "first_name": "Customer",
            "last_name": "Five",
            "email": "customer5@magpie.com",
            "phone_number": "+8801700000005",
            "district": "Khulna",
            "city": "Shib Bari",
            "address": "505 Customer Rd",
            "hashed_password": pw_hash,
            "role": "CUSTOMER"
        }
    ]

    for data in users_data:
        try:
            # Check if user already exists based on email
            existing_user = await db.user.find_unique(where={"email": data["email"]})
            if existing_user:
                print(f"User {data['email']} already exists. Skipping...")
                continue

            await db.user.create(data=data)
            print(f"User {data['email']} ({data['role']}) created successfully.")
        except Exception as e:
            print(f"Failed to create user {data['email']}: {e}")

    await db.disconnect()
    print("\nUser seeding completed!")

if __name__ == "__main__":
    asyncio.run(main())
