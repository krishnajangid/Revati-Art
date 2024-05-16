from typing import List

import sqlalchemy
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi_sqlalchemy import db

from models.users import UsersModel, UserAddressModel
from schema.users import (UserLoginInSchema, UserRegisterInSchema, UserLoginOutSchema, UserMeOutSchema,
                          UserAddressOutSchema)
from utils.auth import (get_password_hash, authenticate_user, create_access_token, get_current_user)

router = APIRouter()


@router.post("/user/login/", response_model=UserLoginOutSchema)
async def user_login_view(user: UserLoginInSchema) -> UserLoginOutSchema:
    user = await authenticate_user(email=user.email, password=user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or Password",
            headers={"Authenticate": "Bearer"}
        )

    response: UserLoginOutSchema = UserLoginOutSchema(
        access_token=await create_access_token(user.id),
        user_id=user.id,
        user_email=user.email
    )
    return response


@router.post("/user/register/", status_code=201)
async def user_register_view(user: UserRegisterInSchema):
    password = get_password_hash(user.password)
    user_obj = UsersModel(
        name=user.name,
        email=user.email,
        password=password,
        is_verified=True
    )
    try:
        db.session.add(user_obj)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    return {}


@router.get("/user/me/", response_model=UserMeOutSchema)
async def user_me_view(user: UsersModel = Depends(get_current_user)) -> UserMeOutSchema:
    response: UserMeOutSchema = UserMeOutSchema(
        id=user.id,
        name=user.name,
        email=user.email,
        mobile=user.mobile,
        profile=user.profile,
        is_verified=user.is_verified,
    )
    return response


@router.get("/user/address/", response_model=List[UserAddressOutSchema])
async def user_me_view(user: UsersModel = Depends(get_current_user)):
    user_address_obj_list = db.session.query(UserAddressModel).filter(UserAddressModel.users_id == user.id).all()

    response_dict_list = []
    for user_address_obj in user_address_obj_list:
        response_dict_list.append({
            "id": user_address_obj.id,
            "city": user_address_obj.city,
            "state": user_address_obj.state,
            "country": user_address_obj.country,
            "zip_code": user_address_obj.zip_code,
            "landmark": user_address_obj.landmark,
            "address_1": user_address_obj.address_1,
            "address_2": user_address_obj.address_2,
            "is_default": user_address_obj.is_default,
            "address_type": user_address_obj.address_type
        })
    return response_dict_list
