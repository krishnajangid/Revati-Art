from typing import List, Optional

from pydantic import BaseModel


class CategoryTagSchema(BaseModel):
    seo_title: Optional[str]
    seo_desc: Optional[str]
    h1_tag: Optional[str]
    h2_tag: Optional[str]
    h3_tag: Optional[str]
    alt_img_tag: Optional[str]


class CategoryOutSchema(BaseModel):
    id: int
    name: str
    description: str
    image: str
    sort_order: Optional[int]
    meta: CategoryTagSchema
    child: List = []
