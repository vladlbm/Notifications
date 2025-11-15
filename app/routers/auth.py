from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.rest_models.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse
from app.services.auth_service import register_user, login_user, refresh_access_token


router = APIRouter()

@router.post("/auth/register", response_model=RegisterResponse)
async def register(request: RegisterRequest) -> RegisterResponse:
    """
    POST /auth/register — регистрация, отдает user_id, access refresh токены.

    :param request: RegisterRequest
    :return: RegisterResponse
    """
    try:
        result = await register_user(request)

        user = result["user"]
        access_token = result["access_token"]
        refresh_token = result["refresh_token"]

        return RegisterResponse(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/login", response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> LoginResponse:
    """
    POST auth/login — отдает access и refresh токены.
    OAuth2 совместимый эндпоинт для Swagger.

    :param form_data: OAuth2PasswordRequestForm
    :return: LoginResponse
    """
    try:
        request = LoginRequest(username=form_data.username, password=form_data.password)
        tokens = await login_user(request)
        return tokens
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/auth/refresh", response_model=RefreshTokenResponse)
async def refresh(request: RefreshTokenRequest) -> RefreshTokenResponse:
    """
    POST /auth/refresh — обновление access токена.

    :param request: RefreshTokenRequest
    :return: RefreshTokenResponse
    """
    tokens = await refresh_access_token(request)
    return RefreshTokenResponse(access_token=tokens["access_token"])
