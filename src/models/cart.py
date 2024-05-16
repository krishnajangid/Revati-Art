from sqlalchemy import (
    Column,
    ForeignKey,
    Integer
)

from models.coupon import CouponModel
from models.product import ProductModel
from models.users import UsersModel
from utils.model_base import Base


class UserCartModel(Base):
    __tablename__ = 'user_cart'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey(ProductModel.id), primary_key=True, nullable=False)
    users_id = Column(Integer, ForeignKey(UsersModel.id), primary_key=True, nullable=False)
    coupon_id = Column(Integer, ForeignKey(CouponModel.id), primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
