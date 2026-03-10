import asyncio
import random
import bcrypt
from prisma import Prisma

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

async def main():
    db = Prisma()
    await db.connect()

    first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
    districts = ["Dhaka", "Chattogram", "Sylhet", "Rajshahi", "Khulna", "Barishal", "Rangpur", "Mymensingh"]
    cities = ["Uttara", "Dhanmondi", "Banani", "Gulshan", "Mirpur", "Panchlaish", "Halishahar", "Zindabazar"]
    streets = ["Lake View Rd", "Park Avenue", "Sector 7", "Road 12", "Green Road", "Station Rd", "New Market", "Hillside Dr"]

    pw_hash = get_password_hash("password123")

    print("Starting to seed 50 customers...")

    for i in range(50):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        district = random.choice(districts)
        city = random.choice(cities)
        street = random.choice(streets)
        
        email = f"{fn.lower()}.{ln.lower()}.{i+1}@example.com"
        phone = f"+8801700{i+10000}" # Hacky unique phone

        try:
            await db.user.create(
                data={
                    "first_name": fn,
                    "last_name": ln,
                    "email": email,
                    "phone_number": phone,
                    "district": district,
                    "city": city,
                    "address": f"{random.randint(1, 999)} {street}",
                    "hashed_password": pw_hash,
                    "role": "CUSTOMER"
                }
            )
            print(f"Customer {i+1}: {fn} {ln} created.")
        except Exception as e:
            print(f"Failed to create customer {i+1}: {e}")

    await db.disconnect()
    print("\nSeeding of 50 customers completed!")

if __name__ == "__main__":
    asyncio.run(main())
