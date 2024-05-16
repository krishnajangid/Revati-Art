from typing import List

from fastapi import APIRouter
from fastapi_sqlalchemy import db

from models.banner import BannerModel
from schema.banner import BannerOutSchema

router = APIRouter()


@router.get("/banner/", response_model=List[BannerOutSchema])
async def get_banner_view() -> List[BannerOutSchema]:
    banner_obj_list = db.session.query(BannerModel).all()

    response_dict_list = []
    for banner_obj in banner_obj_list:
        response_dict_list.append({
            "id": banner_obj.id,
            "image": banner_obj.image,
            "title": banner_obj.title,
            "sub_title": banner_obj.sub_title,
            "sort_order": banner_obj.sort_order,
            "rout_link": banner_obj.rout_link,
            "has_rout_link": True if banner_obj.rout_link else False
        })
    return response_dict_list
