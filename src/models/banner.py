from sqlalchemy import (
    Column,
    Integer,
    String
)

from utils.model_base import Base


class BannerModel(Base):
    __tablename__ = 'banner'

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)
    sub_title = Column(String(255), nullable=True)
    rout_link = Column(String(255), default=True)
    sort_order = Column(Integer, nullable=True)
