from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Boolean,
    Text,
    Enum,
    DECIMAL
)

from utils.model_base import Base


class CouponModel(Base):
    __tablename__ = 'coupon'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(255), nullable=False)
    description = Column(Text)
    active = Column(Boolean, default=False)
    coupon_type = Column(Enum('Amount', 'Percentage'), nullable=False)
    coupon_value = Column(DECIMAL(10, 2), nullable=False)
    sort_order = Column(Integer)
    start_at = Column(DateTime(), default=datetime.utcnow)
    end_at = Column(DateTime(), default=datetime.utcnow)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow)
