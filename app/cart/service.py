from app.db import db
from . import schemas
from fastapi import HTTPException, status

async def get_user_cart(user_id: int):
    items = await db.cartitem.find_many(
        where={"user_id": user_id},
        include={
            "product": {"include": {"variations": True}},
            "variation": True,
            "party_menu": {"include": {"items": {"include": {"product": {"include": {"variations": True}}}}}}
        }
    )
    
    subtotal = 0.0
    for item in items:
        if item.variation:
            subtotal += item.variation.price * item.quantity
        elif item.party_menu:
            subtotal += item.party_menu.price * item.quantity
        elif item.product and not item.variation:
            # Fallback if product has no variation (should not happen in this app's logic)
            pass
            
    return {
        "items": items,
        "subtotal": subtotal,
        "shipping": 0.0,
        "total": subtotal
    }

async def add_to_cart(user_id: int, data: schemas.CartItemCreate):
    # Check if item already exists in cart
    existing_item = await db.cartitem.find_first(
        where={
            "user_id": user_id,
            "product_id": data.product_id,
            "variation_id": data.variation_id,
            "party_menu_id": data.party_menu_id
        }
    )
    
    if existing_item:
        return await db.cartitem.update(
            where={"id": existing_item.id},
            data={"quantity": existing_item.quantity + data.quantity}
        )
    
    return await db.cartitem.create(
        data={
            "user_id": user_id,
            "product_id": data.product_id,
            "variation_id": data.variation_id,
            "party_menu_id": data.party_menu_id,
            "quantity": data.quantity
        }
    )

async def update_cart_item(item_id: int, user_id: int, quantity: int):
    item = await db.cartitem.find_first(where={"id": item_id, "user_id": user_id})
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    
    if quantity <= 0:
        await db.cartitem.delete(where={"id": item_id})
        return None
        
    return await db.cartitem.update(
        where={"id": item_id},
        data={"quantity": quantity}
    )

async def delete_cart_item(item_id: int, user_id: int):
    item = await db.cartitem.find_first(where={"id": item_id, "user_id": user_id})
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    
    await db.cartitem.delete(where={"id": item_id})
    return {"message": "Item removed from cart"}
