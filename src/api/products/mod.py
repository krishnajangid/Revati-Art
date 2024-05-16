from fastapi_sqlalchemy import db

from models.product import ProductModel


class ProductsMod:

    def __init__(self):
        pass

    def get_all_products(self, page, per_page):
        prod_obj = db.session.query(ProductModel).add_columns(
            ProductModel.id,
            ProductModel.name,
            ProductModel.img,
            ProductModel.sku,
            ProductModel.description
        ).filter(
            ProductModel.active == True
        )
        total_result = prod_obj.count()
        prod_obj_list = prod_obj.offset((page * per_page) - per_page).limit(per_page).all()
        result_dict = {
            "page_number": page,
            "page_size": per_page,
            "total": total_result,
            "result": [
                {
                    "id": prod_obj.id,
                    "name": prod_obj.name,
                    "image": prod_obj.img,
                    "description": prod_obj.description,
                    "sku": prod_obj.sku,
                } for prod_obj in prod_obj_list
            ]
        }

        return result_dict
