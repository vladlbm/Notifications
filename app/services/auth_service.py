import logging
from datetime import datetime, timedelta


from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt

from app.db_services.auth import authenticate_user
from app.models.user import User
from app.db_services.users import create_user_db
from app.rest_models.auth import RegisterRequest, LoginRequest, RefreshTokenRequest


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = "secret"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    """
    Генерация access JWT.

    :param data: данные
    :param expires_delta: TL, default = 1 h
    :return: строка с access токеном
    """
    to_encode = data.copy()
    expiration = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=30)) -> str:
    """
    Генерация refresh JWT.

    :param data: данные
    :param expires_delta: TL, default = 1h
    :return: строка с rerfesh токеном.
    """
    to_encode = data.copy()
    expiration = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def register_user(request: RegisterRequest) -> dict:
    """
    Регистрация пользака.

    :param request:
    :return:
    """
    existing_user = await User.get_or_none(username=request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash(request.password)

    user = await create_user_db(request.username, hashed_password)

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    return {"user": user, "access_token": access_token, "refresh_token": refresh_token}


async def login_user(request: LoginRequest) -> dict:
    """
    Логин пользователя.

    :param request:
    :return:
    """
    user = await authenticate_user(request.username, request.password)

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    return {"access_token": access_token, "refresh_token": refresh_token}


def decode_refresh_token(refresh_token: str) -> dict:
    """
    Декодирует refresh токен.

    :param refresh_token: refresh токен
    :return: Декодированные данные токена
    :raises HTTPException: если токен невалиден или истек
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("exp") < datetime.utcnow().timestamp():
            raise HTTPException(status_code=401, detail="Refresh token has expired")

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")


async def refresh_access_token(request: RefreshTokenRequest) -> dict:
    """
    Обновление accesss токена с refresh токеном.

    :param request:
    :return:
    """
    try:
        decoded_token = decode_refresh_token(request.refresh_token)

        user_data = decoded_token.get("sub")

        new_access_token = create_access_token(data={"sub": user_data})

        return {"access_token": new_access_token}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = decode_jwt(token)
        username = payload["sub"]
        user = await User.get_or_none(username=username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except (ExpiredSignatureError, InvalidTokenError):
        raise HTTPException(status_code=401, detail="Could not validate credentials")





