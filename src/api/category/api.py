from fastapi import APIRouter, Depends, Query

from api.category.mod import CategoryMod
from schema.base_schema import PaginationOutSchema, PaginationParamSchema
from schema.category import CategoryOutSchema
from utils.auth import get_current_user

router = APIRouter()


@router.get("/category/", response_model=PaginationOutSchema[CategoryOutSchema])
async def get_all_category_view(
        page_param: PaginationParamSchema = Depends(),
        _=Depends(get_current_user)
) -> PaginationOutSchema[CategoryOutSchema]:
    category_mod_obj = CategoryMod()
    return category_mod_obj.get_all_category(page_param.page, page_param.per_page)
