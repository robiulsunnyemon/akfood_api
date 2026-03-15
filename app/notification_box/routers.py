from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..auth.service import get_current_user
from ..auth.schemas import UserRead
from .schemas import NotificationResponse, NotificationListResponse
from .service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])
service = NotificationService()

@router.get("/", response_model=NotificationListResponse)
async def get_notifications(current_user: UserRead = Depends(get_current_user)):
    notifications = await service.get_user_notifications(current_user.id)
    unread_count = await service.get_unread_count(current_user.id)
    return {"notifications": notifications, "unread_count": unread_count}

@router.put("/{notification_id}/read")
async def mark_as_read(notification_id: int, current_user: UserRead = Depends(get_current_user)):
    await service.mark_as_read(notification_id, current_user.id)
    return {"message": "Notification marked as read"}

@router.put("/read-all")
async def mark_all_as_read(current_user: UserRead = Depends(get_current_user)):
    await service.mark_all_as_read(current_user.id)
    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}")
async def delete_notification(notification_id: int, current_user: UserRead = Depends(get_current_user)):
    await service.delete_notification(notification_id, current_user.id)
    return {"message": "Notification deleted"}
