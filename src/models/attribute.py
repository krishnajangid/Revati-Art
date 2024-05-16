from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from utils.model_base import Base


class AttributeModel(Base):
    __tablename__ = 'attribute'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sort_order = Column(Integer)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow)
