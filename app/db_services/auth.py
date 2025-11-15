from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException

from app.models.user import User
from app.services.utils import verify_password


async def authenticate_user(username: str, password: str) -> User:
    """
    Аутентификация пользака

    :param username:
    :param password:
    :return:
    """
    user = await User.get(username=username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user