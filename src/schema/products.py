from typing import List, Optional

from pydantic import BaseModel


class ProductsOutSchema(BaseModel):
    id: int
    name: str
    description: str
    image: Optional[str]
    sku: Optional[str]
