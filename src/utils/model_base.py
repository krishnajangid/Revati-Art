from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import create_engine

from utils.config import settings

engine = create_engine(
    url="postgresql://{user}:{password}@{host}/{database}?sslmode=require".format(
        user=settings.PG_USER,
        password=settings.PG_PASSWORD,
        database=settings.DB_NAME,
        host=settings.PG_HOST,
    ),
)


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
