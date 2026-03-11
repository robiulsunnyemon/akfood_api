import asyncio
from prisma import Prisma

async def main():
    db = Prisma()
    await db.connect()

    city = "Habiganj"
    locations = [
        "Baitul Aman Jame Masjid",
        "Jagatpur",
        "Mohona Shaistaganj",
        "Krishna Mandeliya",
        "Kolim Nogor Bazar",
        "Bagunipar",
        "N Poly Shaistagonj Depot",
        "Jamotoli",
        "Gowranger Chok",
        "Argon Spinning Mills",
        "Dhariapur Bazar",
        "Shorfabad Shahi Jame Masjid",
        "Dakshin Nurpur Bazar",
        "Dakshin Nurpur",
        "Kodomtoli Uttoron Council",
        "Shaistaganj CNG",
        "Nazma Community",
        "Biye Bari Community Center",
        "Nabatarpur Bazar",
        "Shaistaganj Railway Station",
        "Shaistaganj",
        "Shaistaganj Degree College",
        "Shaistaganj Kamil Madrasa",
        "Morora City",
        "Purbo Morora Jame Mosjid",
        "Morora Road",
        "Nishapat Ideal High School",
        "Nishapot Eidgah",
        "Pran Dist Chunarughat",
        "Ulukandi Pashchim Jame Mosque",
        "Kodomtoli Central Jame Mosque",
        "Ulukandi Adarsh Shikhan Academy",
        "Borompur Bazar",
        "M/s Chowdhury Filling Station",
        "M/S V I P Bricks",
        "Shaistaganj Model Kamil Madrasah",
        "Zohur Chan Bibi Mohila College",
        "Bagunipara Eidgah",
        "Ayesha Jame Mosque",
        "Baitul Mamur Jame Mosjid",
        "Shaistaganj Puran Bazar"
    ]

    print(f"Seeding delivery area for {city} with {len(locations)} locations...")
    
    # Check if exists
    existing = await db.deliveryarea.find_unique(where={"city": city})
    if existing:
        print(f"City {city} already exists. Updating locations...")
        await db.deliveryarea.update(
            where={"city": city},
            data={"locations": locations}
        )
    else:
        print(f"Creating city {city}...")
        await db.deliveryarea.create(
            data={
                "city": city,
                "locations": locations
            }
        )
        
    print("Done!")
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
