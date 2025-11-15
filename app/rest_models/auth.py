from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """
    Для регистрации пользователя.
    """
    username: str
    password: str


class RegisterResponse(BaseModel):
    """
    Ответ на регистрацию.
    """
    user_id: int
    access_token: str
    refresh_token: str


class LoginRequest(BaseModel):
    """
    Для логина пользователя.
    """
    username: str
    password: str


class LoginResponse(BaseModel):
    """
    Ответ при логине.
    """
    access_token: str
    refresh_token: str


class RefreshTokenRequest(BaseModel):
    """
    Запрос на обновление токена.
    """
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """
    Ответ на обновление токено.
    """
    access_token: str