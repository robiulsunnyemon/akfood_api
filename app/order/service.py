from prisma import Prisma
from typing import List, Optional
from datetime import datetime
from app.db import db
from app.order.schemas import OrderCreate, OrderStatus

async def create_order(user_id: int, order_data: dict) -> dict:
    if not db.is_connected():
        await db.connect()

    # 1. Get user's cart items
    cart_items = await db.cartitem.find_many(
        where={"user_id": user_id},
        include={
            "product": True,
            "variation": True,
            "party_menu": True
        }
    )

    if not cart_items:
        raise Exception("Cart is empty")

    # 2. Get the current delivery fee
    delivery_fee_record = await db.deliveryfee.find_first()
    delivery_fee = delivery_fee_record.fee if delivery_fee_record else 0.0

    # 3. Calculate subtotal
    subtotal = 0.0
    order_items_to_create = []

    for item in cart_items:
        item_name = ""
        item_price = 0.0
        
        if item.party_menu:
            item_name = item.party_menu.title
            item_price = item.party_menu.price
        elif item.variation:
            item_name = f"{item.product.name} ({item.variation.name})"
            item_price = item.variation.price
        else:
            item_name = item.product.name
            # Fallback if no variation (though schema usually has variations or party menu)
            item_price = 0.0 

        subtotal += item_price * item.quantity
        
        order_items_to_create.append({
            "product_id": item.product_id,
            "variation_id": item.variation_id,
            "party_menu_id": item.party_menu_id,
            "name": item_name,
            "price": item_price,
            "quantity": item.quantity
        })

    total = subtotal + delivery_fee

    # 4. Create Order and OrderItems in a transaction
    async with db.tx() as transaction:
        # Create Order
        new_order = await transaction.order.create(
            data={
                "user_id": user_id,
                "city": order_data["city"],
                "location": order_data["location"],
                "address": order_data["address"],
                "special_instruction": order_data.get("special_instruction"),
                "phone_number": order_data["phone_number"],
                "payment_method": order_data["payment_method"],
                "subtotal": subtotal,
                "delivery_fee": delivery_fee,
                "total": total,
                "status": "PENDING",
                "items": {
                    "create": order_items_to_create
                }
            },
            include={"items": True}
        )
        
        # 5. Clear Cart
        await transaction.cartitem.delete_many(where={"user_id": user_id})
        
        return new_order.model_dump()

async def get_user_orders(user_id: int) -> List[dict]:
    if not db.is_connected():
        await db.connect()
    orders = await db.order.find_many(
        where={"user_id": user_id},
        include={"items": True},
        order={"created_at": "desc"}
    )
    return [order.model_dump() for order in orders]

async def get_all_orders() -> List[dict]:
    if not db.is_connected():
        await db.connect()
    orders = await db.order.find_many(
        include={
            "items": True,
            "user": True
        },
        order={"created_at": "desc"}
    )
    return [order.model_dump() for order in orders]

async def update_order_status(order_id: int, status: str) -> Optional[dict]:
    if not db.is_connected():
        await db.connect()
    updated = await db.order.update(
        where={"id": order_id},
        data={"status": status},
        include={"items": True}
    )
    return updated.model_dump() if updated else None

async def delete_order(order_id: int) -> bool:
    if not db.is_connected():
        await db.connect()
    await db.order.delete(where={"id": order_id})
    return True
