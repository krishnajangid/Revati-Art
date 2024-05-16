from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Boolean,
    Text
)


from utils.model_base import Base


class CategoryModel(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey("category.id"), primary_key=True, nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String(255), nullable=True)
    sort_order = Column(Integer)
    active = Column(Boolean, default=False)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow)

    def __str__(self):
        return self.name

