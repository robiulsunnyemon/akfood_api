from app.db import db
from . import schemas
from fastapi import HTTPException, status

async def get_all_products(skip: int = 0, take: int = 21):
    where_input = {"is_active": True}
    total = await db.product.count(where=where_input)
    items = await db.product.find_many(
        where=where_input,
        skip=skip,
        take=take,
        include={"variations": True, "category": True},
        order={"created_at": "desc"}
    )
    return {"items": items, "total": total}

async def create_product(data: schemas.ProductCreate):
    # Create the product first
    product = await db.product.create(
        data={
            "name": data.name,
            "description": data.description,
            "image_url": data.image_url,
            "category": {"connect": {"id": data.category_id}},
            "variations": {
                "create": [variation.dict() for variation in data.variations]
            }
        },
        include={"variations": True}
    )
    return product

async def get_product_by_id(product_id: int):
    product = await db.product.find_first(where={"id": product_id, "is_active": True}, include={"variations": True})
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

async def update_product(product_id: int, data: schemas.ProductUpdate):
    # Prepare update data
    update_data = {}
    if data.name is not None: update_data["name"] = data.name
    if data.description is not None: update_data["description"] = data.description
    if data.image_url is not None: update_data["image_url"] = data.image_url
    if data.category_id is not None: 
        update_data["category"] = {"connect": {"id": data.category_id}}
    
    # Handle variations if provided (easiest way is to delete and recreate for this simple case, 
    # or match by ID if we want to be more precise. Let's replace for now to simplify).
    if data.variations is not None:
        await db.productvariation.delete_many(where={"product_id": product_id})
        update_data["variations"] = {
            "create": [{"name": v.name, "price": v.price} for v in data.variations]
        }

    product = await db.product.update(
        where={"id": product_id},
        data=update_data,
        include={"variations": True}
    )
    return product

async def delete_product(product_id: int):
    # Instead of deleting variations and the product itself, we perform a soft delete
    # to maintain data integrity for existing orders and party menus.
    await db.product.update(
        where={"id": product_id},
        data={"is_active": False}
    )
    return {"message": "Product soft-deleted successfully"}
