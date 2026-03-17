import asyncio
from prisma import Prisma

async def destroy_database():
    print("\n" + "!" * 50)
    print("⚠️  CRITICAL WARNING: DATABASE DESTRUCTION ⚠️")
    print("This script will DELETE ALL TABLES and ALL DATA permanently.")
    print("This action is NOT REVERSIBLE.")
    print("!" * 50 + "\n")
    
    confirm = input("Are you absolutely sure you want to proceed? Type 'DESTROY' to confirm: ")
    
    if confirm != 'DESTROY':
        print("\n❌ Destruction cancelled. No changes were made.")
        return

    print("\n🚀 Starting database destruction...")
    db = Prisma()
    await db.connect()

    try:
        # We use raw SQL to drop the entire public schema and recreate it
        # This is the fastest way to wipe everything (tables, indexes, types, etc.)
        print("- Dropping public schema...")
        await db.execute_raw('DROP SCHEMA public CASCADE;')
        
        print("- Recreating public schema...")
        await db.execute_raw('CREATE SCHEMA public;')
        
        print("- Granting permissions (Standard for PostgreSQL)...")
        await db.execute_raw('GRANT ALL ON SCHEMA public TO postgres;')
        await db.execute_raw('GRANT ALL ON SCHEMA public TO public;')

        print("\n🔥 SUCCESS: The database has been completely wiped clean!")
        print("💡 NOTE: You must run 'prisma db push' or your migration scripts to recreate the tables.")
        
    except Exception as e:
        print(f"\n❌ ERROR during destruction: {e}")
    finally:
        await db.disconnect()
        print("\nDatabase connection closed.")

if __name__ == "__main__":
    asyncio.run(destroy_database())
