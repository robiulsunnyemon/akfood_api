from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class NotificationType(str, Enum):
    ORDER = "ORDER"
    PROFILE = "PROFILE"
    ACCOUNT = "ACCOUNT"

class NotificationBase(BaseModel):
    title: str
    message: str
    type: NotificationType = NotificationType.ORDER

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponse]
    unread_count: int
