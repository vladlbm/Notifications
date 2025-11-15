from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.notification import Notification
from app.models.user import User
from app.rest_models.notifications import NotificationCreate, NotificationResponse
from app.services.notifications_service import create_notification, get_notifications, delete_notification
from app.services.auth_service import get_current_user, oauth2_scheme

router = APIRouter()

@router.post("/notifications/", response_model=NotificationResponse)
async def create_new_notification(
    notification: NotificationCreate,
    current_user: User = Depends(get_current_user),
) -> NotificationResponse:
    """
    POST /notifications/ — создать уведомление с присвоением к текущему юзеру user_id извлекается из JWT access-токена.

    :param notification:
    :param current_user:
    :return:
    """
    print(current_user.id)

    return await create_notification(notification, current_user)

@router.get("/notifications/", response_model=List[NotificationResponse])
async def get_user_notifications(
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(get_current_user)
) -> List[NotificationResponse]:
    """
    GET /notifications/ — список своих уведомлений (limit, offset пагинация)

    :param limit:
    :param offset:
    :param current_user:
    :return:
    """
    return await get_notifications(current_user, limit=limit, offset=offset)

@router.delete("/notifications/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_notification(
    id: int,
    current_user: User = Depends(get_current_user)
) -> None:
    """
    DELETE /notifications/{id} — удаление своих уведомлений

    :param id:
    :param current_user:
    :return:
    """
    await delete_notification(id, current_user)
