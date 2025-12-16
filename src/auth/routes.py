from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import UserCreateModel, UserModel
from .service import UserService
form .utils import create_access_token, decode_token

auth_router = APIRouter()
user_service = UserService()

@auth_router.post(
    "/signup",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    if await user_service.user_exists(email, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email already exists"
        )

    return await user_service.create_user(user_data, session)

@auth_router.post(
    "/login"
)
async def login_users():
    