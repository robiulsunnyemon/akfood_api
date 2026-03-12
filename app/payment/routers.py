from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
from typing import List
from app.auth.service import get_current_user, get_admin_user
from . import service, schemas

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/stats", response_model=schemas.PaymentStats)
async def get_stats(admin=Depends(get_admin_user)):
    return await service.get_payment_stats()

@router.get("/transactions", response_model=List[schemas.TransactionResponse])
async def get_transactions(admin=Depends(get_admin_user)):
    return await service.get_all_transactions()

@router.post("/initiate")
async def initiate_payment(
    data: schemas.PaymentSessionCreate, 
    user=Depends(get_current_user)
):
    url = await service.initiate_order_payment(data.order_id, user.id)
    if not url:
        raise HTTPException(status_code=400, detail="Failed to initiate payment")
    return {"url": url}

@router.post("/success")
async def payment_success(
    request: Request,
    tran_id: str = Form(...),
    val_id: str = Form(...)
):
    # This is called by SSLCommerz as a POST request
    success = await service.verify_payment(tran_id, val_id)
    if success:
        # Redirect to a success page or just return success
        return {"status": "success", "message": "Payment verified"}
    return {"status": "failed", "message": "Payment verification failed"}

@router.post("/fail")
async def payment_fail(tran_id: str = Form(...)):
    # Update order with FAILED status
    from app.db import db
    await db.order.update(
        where={"transaction_id": tran_id},
        data={"payment_status": "FAILED"}
    )
    return {"status": "failed", "message": "Payment failed"}

@router.post("/cancel")
async def payment_cancel(tran_id: str = Form(...)):
    from app.db import db
    await db.order.update(
        where={"transaction_id": tran_id},
        data={"payment_status": "CANCELLED"}
    )
    return {"status": "cancelled", "message": "Payment cancelled"}

@router.post("/ipn")
async def payment_ipn(
    tran_id: str = Form(...),
    val_id: str = Form(...),
    status: str = Form(...)
):
    # Instant Payment Notification
    if status == "VALID":
        await service.verify_payment(tran_id, val_id)
    return {"status": "received"}
