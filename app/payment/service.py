from datetime import datetime
from typing import List, Optional
from app.db import db
from .schemas import PaymentStats, TransactionResponse
from app.utils.ssl_service import ssl_service
from app.order.service import get_user_orders

async def get_payment_stats() -> PaymentStats:
    # In a real app, we would sum up from a Transaction table.
    # For now, we calculate from PAID orders.
    # SSL Fee is usually around 2.5% to 3.5%. Let's assume 3.0% for calculation.
    
    orders = await db.order.find_many(
        where={"payment_status": "PAID"}
    )
    
    total_paid_amount = sum(order.total for order in orders)
    ssl_fee_rate = 0.03 # 3%
    total_ssl_cost = total_paid_amount * ssl_fee_rate
    net_revenue = total_paid_amount - total_ssl_cost
    
    return PaymentStats(
        platform_earnings=total_paid_amount,
        total_revenue=net_revenue,
        ssl_cost=total_ssl_cost
    )

async def get_all_transactions() -> List[dict]:
    # We fetch orders that have a transaction_id
    orders = await db.order.find_many(
        where={
            "transaction_id": {"not": None}
        },
        include={"user": True},
        order={"created_at": "desc"}
    )
    
    transactions = []
    for order in orders:
        transactions.append({
            "id": order.id,
            "order_id": order.id,
            "amount": order.total,
            "transaction_id": order.transaction_id,
            "status": order.payment_status,
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
        # Update order status
        await db.order.update(
            where={"transaction_id": tran_id},
            data={
                "payment_status": "PAID"
            }
        )
        return True
    return False
