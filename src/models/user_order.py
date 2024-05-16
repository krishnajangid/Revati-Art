from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    DECIMAL
)

from models.coupon import CouponModel
from models.product import ProductModel
from models.users import UsersModel
from utils.model_base import Base


class OrderStatusModel(Base):
    __tablename__ = 'order_status'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)


class UserOrderModel(Base):
    __tablename__ = 'user_order'

    id = Column(Integer, primary_key=True, index=True)
    users_id = Column(Integer, ForeignKey(UsersModel.id), primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey(ProductModel.id), primary_key=True, nullable=False)
    coupon_id = Column(Integer, ForeignKey(CouponModel.id), primary_key=True, nullable=False)
    order_status_id = Column(Integer, ForeignKey(OrderStatusModel.id), primary_key=True, nullable=False)
    delivery_charge = Column(DECIMAL(10, 2), nullable=False)
    payment_mode = Column(String(50), nullable=True)
    transaction_id = Column(String(50), nullable=True)
    delivery_at = Column(DateTime())
    order_at = Column(DateTime(), default=datetime.utcnow)


class OrderProductModel(Base):
    __tablename__ = 'order_product'

    id = Column(Integer, primary_key=True, index=True)
    user_order_id = Column(Integer, ForeignKey(UserOrderModel.id), primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey(ProductModel.id), primary_key=True, nullable=False)
    product_name = Column(String(50), nullable=True)
    quantity = Column(Integer, nullable=False)
    product_price = Column(DECIMAL(10, 2), nullable=True)
    discount_price = Column(DECIMAL(10, 2), nullable=True)
    tax_percentage = Column(DECIMAL(10, 2), nullable=True)
    total_amount = Column(DECIMAL(10, 2), nullable=True)
