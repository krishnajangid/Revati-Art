from typing import Union, Optional

from pydantic import BaseModel, EmailStr


class UserLoginInSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@gmail.com",
                "password": "test@123"
            }
        }


class UserLoginOutSchema(BaseModel):
    access_token: str
    user_id: int
    user_email: str


class UserRegisterInSchema(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserMeOutSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    mobile: Optional[int]
    profile: Optional[str]
    is_verified: bool


class UserAddressOutSchema(BaseModel):
    id: int
    city: str
    state: str
    country: str
    zip_code: str
    landmark: Optional[str]
    address_1: str
    address_2: Optional[str]
    is_default: str
    address_type: str
