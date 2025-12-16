from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import UserCreateModel, UserModel,UserLoginModel
from .service import UserService
from .utils import create_access_token, decode_token
from datetime import timedelta
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = UserService()
REFRESH_TOKEN_EXPIRY=2

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
async def login_users(
    login_data:UserLoginModel,session:AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email,session)

    if user is not None:
        password_valid = verify_password(password,user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_id': str(user.uid)
                }
            )

            refresh_token = create_access_token(
                user_data ={
                    'email': user.email,
                    'user_id': str(user.uid),
                    refresh=True,
                    expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)       
                }
            )

            return JSONResponse(
                content={
                    "message":"Login Successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )
    raise HTTPException(status_code=status.status.HTTP_401_UNAUTHORIZED,detail="Invalid Email Or Password")
