from datetime import datetime, timedelta

import jwt
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from fastapi_sqlalchemy import db
from passlib.context import CryptContext

from models.users import UsersModel
import logging
from utils.config import settings

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str):
    user: UsersModel = db.session.query(UsersModel).filter(UsersModel.email == email).one()
    if user and verify_password(password, user.password):
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not verified",
                headers={"Authenticate": "Bearer"}
            )
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Username or Password",
        headers={"Authenticate": "Bearer"}
    )


async def create_access_token(user_id) -> str:
    user: UsersModel = db.session.query(UsersModel).filter(UsersModel.id == user_id).one()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or Password",
            headers={"Authenticate": "Bearer"}
        )

    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "id": user.id,
        "username": user.name,
        "email": user.email,
        "exp": expire
    }
    encoded_jwt = jwt.encode(token_data, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def very_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    except Exception as e:
        logging.info(f"Error while verifying token. Error {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"Authenticate": "Bearer"}
        )
    user = db.session.query(UsersModel).filter(UsersModel.id == payload["id"]).one()
    return user


async def get_current_user(token=Depends(HTTPBearer())):
    return await very_token(token.credentials)
