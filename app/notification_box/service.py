from typing import List
from app.db import db
from .schemas import NotificationType

class NotificationService:
    async def get_user_notifications(self, user_id: int) -> List:
        return await db.notification.find_many(
            where={"user_id": user_id},
            order={"created_at": "desc"}
        )

    async def get_unread_count(self, user_id: int) -> int:
        return await db.notification.count(
            where={
                "user_id": user_id,
                "is_read": False
            }
        )

    async def create_notification(self, user_id: int, title: str, message: str, type: NotificationType):
        return await db.notification.create(
            data={
                "user_id": user_id,
                "title": title,
                "message": message,
                "type": type
            }
        )

    async def mark_as_read(self, notification_id: int, user_id: int):
        return await db.notification.update_many(
            where={
                "id": notification_id,
                "user_id": user_id
            },
            data={"is_read": True}
        )

    async def mark_all_as_read(self, user_id: int):
        return await db.notification.update_many(
            where={"user_id": user_id},
            data={"is_read": True}
        )

    async def delete_notification(self, notification_id: int, user_id: int):
        # prisma python delete doesn't return count easily with delete_many for all engines
        # but delete_many is appropriate for batch deleting with user control
        return await db.notification.delete_many(
            where={
                "id": notification_id,
                "user_id": user_id
            }
        )
