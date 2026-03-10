from app.db import db
from . import schemas
from fastapi import HTTPException, status
from typing import List

async def get_all_party_menus(skip: int = 0, take: int = 21):
    total = await db.partymenu.count()
    items = await db.partymenu.find_many(
        skip=skip,
        take=take,
        include={"items": {"include": {"product": {"include": {"variations": True}}}}},
        order={"created_at": "desc"}
    )
    return {"items": items, "total": total}

async def get_party_menu_by_id(menu_id: int):
    menu = await db.partymenu.find_unique(
        where={"id": menu_id},
        include={"items": {"include": {"product": {"include": {"variations": True}}}}}
    )
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Party Menu not found")
    return menu

async def create_party_menu(data: schemas.PartyMenuCreate):
    # Create the party menu
    party_menu = await db.partymenu.create(
        data={
            "title": data.title,
            "description": data.description,
            "image_url": data.image_url,
            "price": data.price,
            "category": data.category,
            "items": {
                "create": [{"product_id": pid} for pid in data.product_ids]
            }
        },
        include={"items": {"include": {"product": {"include": {"variations": True}}}}}
    )
    return party_menu

async def update_party_menu(menu_id: int, data: schemas.PartyMenuUpdate):
    # Check if menu exists
    await get_party_menu_by_id(menu_id)
    
    update_data = {}
    if data.title is not None: update_data["title"] = data.title
    if data.description is not None: update_data["description"] = data.description
    if data.image_url is not None: update_data["image_url"] = data.image_url
    if data.price is not None: update_data["price"] = data.price
    if data.category is not None: update_data["category"] = data.category

    if data.product_ids is not None:
        # Simple approach: clear and recreate items
        await db.partymenuitem.delete_many(where={"party_menu_id": menu_id})
        update_data["items"] = {
            "create": [{"product_id": pid} for pid in data.product_ids]
        }

    party_menu = await db.partymenu.update(
        where={"id": menu_id},
        data=update_data,
        include={"items": {"include": {"product": {"include": {"variations": True}}}}}
    )
    return party_menu

async def delete_party_menu(menu_id: int):
    # PartyMenuItems are deleted automatically due to Cascase Delete in schema
    await db.partymenu.delete(where={"id": menu_id})
    return {"message": "Party Menu deleted successfully"}
