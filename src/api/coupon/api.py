from datetime import datetime
from typing import List

from fastapi import APIRouter
from fastapi_sqlalchemy import db

from models.coupon import CouponModel
from schema.coupon import CouponOutSchema

router = APIRouter()


@router.get("/coupon/", response_model=List[CouponOutSchema])
async def get_coupon_view():
    coupon_obj_list = db.session.query(CouponModel).filter(
        CouponModel.active == True,
        CouponModel.start_at <= datetime.today().date(),
        CouponModel.end_at >= datetime.today().date(),
    ).all()

    coupon_dict_list = []
    for coupon_obj in coupon_obj_list:
        coupon_dict_list.append({
            "id": coupon_obj.id,
            "code": coupon_obj.code,
            "sort_order": coupon_obj.sort_order,
            "coupon_type": coupon_obj.coupon_type,
            "coupon_value": coupon_obj.coupon_value,
            "description": coupon_obj.description,
        })

    return coupon_dict_list
