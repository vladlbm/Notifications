from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NotificationType(str, Enum):
    """
    Типы уведомлений.
    """
    like = "like"
    comment = "comment"
    repost = "repost"


class NotificationCreate(BaseModel):
    """
    Для создания нового уведомления.
    """
    type: NotificationType
    text: str


class NotificationResponse(BaseModel):
    """
    Для получения уведомлений.
    """
    id: int
    user_id: int
    type: NotificationType
    text: str
    created_at: datetime
    username: str
    avatar_url: str

    class Config:
        from_attributes = True
