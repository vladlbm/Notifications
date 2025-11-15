from datetime import datetime
from enum import Enum

from tortoise import fields, models

from .user import User


class NotificationType(str, Enum):
    """
    `type: str`— одно из Enum:`like`,`comment`,`repost`
    """
    like = "like"
    comment = "comment"
    repost = "repost"


class Notification(models.Model):
    """
    - `id: int`
    - `user_id: int`
    - `type: str`— одно из Enum:`like`,`comment`,`repost`
    - `text: str`
    - `created_at: datetime`
    """
    id = fields.IntField(pk=True, generated=True)
    user = fields.ForeignKeyField("models.User", related_name="notifications")
    type = fields.CharEnumField(NotificationType)
    text = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

