from datetime import datetime

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Boolean,
    Text
)
from sqlalchemy.orm import relationship

from models.category import CategoryModel
from utils.model_base import Base


class ProductModel(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey(CategoryModel.id), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    sku = Column(String(10), nullable=False)
    description = Column(Text, nullable=False)
    img = Column(FileType(storage=FileSystemStorage(path="/tmp")))
    active = Column(Boolean, default=False)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow)

    category = relationship("CategoryModel")

    def __str__(self):
        return self.name
