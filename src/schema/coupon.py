from typing import Optional

from pydantic import BaseModel


class CouponOutSchema(BaseModel):
    id: int
    code: str
    sort_order: Optional[int]
    coupon_type: str
    coupon_value: int
    description: Optional[str]
