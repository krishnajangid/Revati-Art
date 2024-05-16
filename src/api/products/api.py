from fastapi import APIRouter, Depends, Query

from api.products.mod import ProductsMod
from schema.base_schema import PaginationOutSchema, PaginationParamSchema
from schema.products import ProductsOutSchema
from utils.auth import get_current_user

router = APIRouter()


@router.get("/products/", response_model=PaginationOutSchema[ProductsOutSchema])
async def get_all_products_view(
        page_param: PaginationParamSchema = Depends(),
        _=Depends(get_current_user)
) -> PaginationOutSchema[ProductsOutSchema]:
    mod_obj = ProductsMod()
    return mod_obj.get_all_products(page_param.page, page_param.per_page)
