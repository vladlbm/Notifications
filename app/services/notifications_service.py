
from datetime import datetime
from fastapi import HTTPException, status

from app.db_services.notifications import create_notification_db, get_user_notifications_db, delete_notification_db
from app.models.notification import Notification
from app.models.user import User
from app.rest_models.notifications import NotificationCreate, NotificationResponse


async def create_notification(
        notification_data: NotificationCreate,
        user: User
) -> NotificationResponse:
    """
    Создание уведомления.

    :param notification_data:
    :param user:
    :return:
    """
    notification = await create_notification_db(user, notification_data)
    await notification.fetch_related('user')

    return NotificationResponse(
        id=notification.id,
        user_id=notification.user.id,
        type=notification.type,
        text=notification.text,
        created_at=notification.created_at,
        username=notification.user.username,
        avatar_url=notification.user.avatar_url
    )


async def get_notifications(
    user: User, limit: int = 10, offset: int = 0
) -> list[NotificationResponse]:
    """
    Получение уведомлений.

    :param user:
    :param limit:
    :param offset:
    :return:
    """
    notifications = await get_user_notifications_db(user, limit, offset)
    return [
        NotificationResponse(
            id=notification.id,
            user_id=notification.user.id,
            type=notification.type,
            text=notification.text,
            created_at=notification.created_at,
            username=notification.user.username,
            avatar_url=notification.user.avatar_url
        )
        for notification in notifications
    ]


async def delete_notification(id: int, user: User) -> None:
    """
    Удаление уведомления.

    :param id:
    :param user:
    :return:
    """
    notification = await Notification.get_or_none(id=id, user_id=user.id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    await delete_notification_db(id, user)
