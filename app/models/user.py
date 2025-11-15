from datetime import datetime

from tortoise import fields, models


class User(models.Model):
    """
    - `id: int`
    - `username: str`
    - `avatar_url: str`— захардкожен
    - `created_at: datetime`
    """
    id = fields.IntField(pk=True, generated=True)
    username = fields.CharField(max_length=255, unique=True)
    avatar_url = fields.CharField(max_length=255, default="://link")
    created_at = fields.DatetimeField(auto_now_add=True)
    password = fields.CharField(max_length=255)