from tortoise.exceptions import DoesNotExist, IntegrityError
from fastapi import HTTPException

from app.models.user import User


async def create_user_db(username: str, hashed_password: str) -> User:
    """
    Создание пользователя в БД

    :param username:
    :param password:
    :param email:
    :return:
    """
    try:
        user = await User.create(username=username, password=hashed_password)
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Пользак существует")
