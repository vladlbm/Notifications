from datetime import datetime

from tortoise.exceptions import DoesNotExist

from app.models.notification import Notification
from app.models.user import User
from app.rest_models.notifications import NotificationCreate


async def create_notification_db(user: User, notification_data: NotificationCreate) -> Notification:
    """
    Создание уведомления в БД

    :param user:
    :param notification_data:
    :return:
    """
    print(user.id)
    notification = await Notification.create(
        user_id=user.id,
        type=notification_data.type,
        text=notification_data.text,
        created_at=datetime.utcnow()
    )
    return notification


async def get_user_notifications_db(user: User, limit: int = 10, offset: int = 0):
    """
    Получение уведомлений пользователя с БД

    :param user:
    :param limit:
    :param offset:
    :return:
    """
    return await Notification.filter(user_id=user.id) \
        .order_by("-created_at") \
        .offset(offset) \
        .limit(limit) \
        .prefetch_related("user")


async def delete_notification_db(notification_id: int, user: User):
    """
    Удаление уведомлений из БД

    :param notification_id:
    :param user:
    :return:
    """
    notification = await Notification.get_or_none(id=notification_id, user_id=user.id)
    if notification:
        await notification.delete()
