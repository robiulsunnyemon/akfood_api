from app.db import db
from . import schemas
from typing import List

async def get_all_categories() -> List[schemas.CategoryRead]:
    return await db.category.find_many(order={"name": "asc"})

async def create_category(data: schemas.CategoryCreate) -> schemas.CategoryRead:
    return await db.category.create(
        data={
            "name": data.name,
            "image_url": data.image_url
        }
    )
