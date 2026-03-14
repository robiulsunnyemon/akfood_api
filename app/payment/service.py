from datetime import datetime
from typing import List, Optional
from app.db import db
from .schemas import PaymentStats, TransactionResponse
from app.utils.ssl_service import ssl_service
from app.order.service import get_user_orders

async def get_payment_stats() -> PaymentStats:
    # Get all successful Digital Payments
    digital_orders = await db.order.find_many(
        where={
            "payment_method": "Digital Payment",
            "payment_status": "PAID"
        }
    )
    
    # Get all COD orders that are DELIVERED
    cod_orders = await db.order.find_many(
        where={
            "payment_method": "Cash on delivery",
            "status": "DELIVERED"
        }
    )
    
    # Calculate online revenue and SSL cost
    online_revenue = sum(order.total for order in digital_orders)
    ssl_fee_rate = 0.03 # 3%
    total_ssl_cost = online_revenue * ssl_fee_rate
    
    # Calculate offline revenue
    offline_revenue = sum(order.total for order in cod_orders)
    
    # Total revenue is sum of all, minus ssl cost for digital
    total_revenue = (online_revenue - total_ssl_cost) + offline_revenue
    
    return PaymentStats(
        total_revenue=total_revenue,
        offline_revenue=offline_revenue,
        online_revenue=online_revenue,
        ssl_cost=total_ssl_cost
    )

async def get_all_transactions() -> List[dict]:
    # We fetch digital orders that have a transaction_id and all COD orders
    orders = await db.order.find_many(
        where={
            "OR": [
                {"transaction_id": {"not": None}},
                {"payment_method": "Cash on delivery"}
            ]
        },
        include={"user": True},
        order={"created_at": "desc"}
    )
    
    transactions = []
    for order in orders:
        # Determine display status for COD pending vs delivered etc
        display_status = order.payment_status
        if order.payment_method == "Cash on delivery":
            if order.status == "DELIVERED" or order.payment_status == "PAID":
                display_status = "PAID"
            elif order.status == "CANCELLED":
                display_status = "CANCELLED"
            else:
                display_status = "PENDING"
                
        transactions.append({
            "id": order.id,
            "order_id": order.id,
            "amount": order.total,
            "transaction_id": order.transaction_id if order.transaction_id else f"COD_{order.id}",
            "status": display_status,
            "created_at": order.created_at,
            "customer_name": f"{order.user.first_name} {order.user.last_name}" if order.user else "Unknown"
        })
    return transactions

async def initiate_order_payment(order_id: int, user_id: int) -> Optional[str]:
    order = await db.order.find_unique(
        where={"id": order_id},
        include={"user": True}
    )
    
    if not order or order.user_id != user_id:
        return None
        
    tran_id = f"TXN_{order.id}_{int(datetime.now().timestamp())}"
    
    # Update order with transaction_id (as pending)
    await db.order.update(
        where={"id": order_id},
        data={"transaction_id": tran_id}
    )
    
    response = await ssl_service.initiate_payment(
        total_amount=order.total,
        tran_id=tran_id,
        cus_name=f"{order.user.first_name} {order.user.last_name}",
        cus_email=order.user.email,
        cus_phone=order.phone_number or "01XXXXXXXXX"
    )
    
    if response and response.get("status") == "SUCCESS":
        return response.get("GatewayPageURL")
    return None

async def verify_payment(tran_id: str, val_id: str):
    # This is called by SSLCommerz on success
    validation = await ssl_service.validate_payment(val_id)
    
    if validation and validation.get("status") == "VALID":
        # Update order status to PAID
        updated_order = await db.order.update(
            where={"transaction_id": tran_id},
            data={
                "payment_status": "PAID"
            }
        )
        # Now clear the cart for the user since payment is confirmed
        if updated_order:
            await db.cartitem.delete_many(where={"user_id": updated_order.user_id})
        return True
    return False
