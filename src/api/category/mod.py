from fastapi_sqlalchemy import db

from models.category import CategoryModel


class CategoryMod:

    def __init__(self):
        pass

    def get_all_category(self, page, per_page):
        category_obj = db.session.query(CategoryModel).add_columns(
            CategoryModel.id,
            CategoryModel.name,
            CategoryModel.image,
            CategoryModel.sort_order,
            CategoryModel.description
        ).filter(
            CategoryModel.active == True,
            CategoryModel.parent_id == None
        )
        total_result = category_obj.count()
        category_obj_list = category_obj.offset((page * per_page) - per_page).limit(per_page).all()
        result_dict = {
            "page_number": page,
            "page_size": per_page,
            "total": total_result,
            "result": self.__get_category(category_obj_list)
        }

        return result_dict

    def __get_category(self, category_obj_list):
        category_dict_list = []
        for category_obj in category_obj_list:
            child_category_obj = db.session.query(CategoryModel).join(
                CategoryTagModel, isouter=True
            ).add_columns(
                CategoryModel.id,
                CategoryModel.name,
                CategoryModel.image,
                CategoryModel.sort_order,
                CategoryModel.description,
                CategoryTagModel.seo_title,
                CategoryTagModel.seo_desc,
                CategoryTagModel.h1_tag,
                CategoryTagModel.h2_tag,
                CategoryTagModel.h3_tag,
                CategoryTagModel.alt_img_tag,
            ).filter(
                CategoryModel.parent_id == category_obj.id,
                CategoryModel.active == True
            ).all()
            child_data_list = self.__get_category(child_category_obj)
            category_dict_list.append({
                "id": category_obj.id,
                "name": category_obj.name,
                "image": category_obj.image,
                "description": category_obj.description,
                "sort_order": category_obj.sort_order,
                "meta": {
                    "seo_title": category_obj.seo_title,
                    "seo_desc": category_obj.seo_desc,
                    "h1_tag": category_obj.h1_tag,
                    "h2_tag": category_obj.h2_tag,
                    "h3_tag": category_obj.h3_tag,
                    "alt_img_tag": category_obj.alt_img_tag,
                },
                "child": child_data_list
            })
        return category_dict_list
