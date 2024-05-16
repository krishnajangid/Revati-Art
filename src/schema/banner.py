from typing import Optional

from pydantic import BaseModel


class BannerOutSchema(BaseModel):
    id: int
    image: str
    title: Optional[str]
    sub_title: Optional[str]
    sort_order: Optional[int]
    rout_link: Optional[str]
    has_rout_link: bool
