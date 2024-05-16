from sqladmin import ModelView

from models.category import CategoryModel
from models.product import ProductModel
from models.users import UsersModel


class UserAdmin(ModelView, model=UsersModel):
    name_plural = "Users"
    can_export = False
    column_searchable_list = [UsersModel.email]
    column_list = [UsersModel.id, UsersModel.name, UsersModel.email, UsersModel.created_at]


class CategoryAdmin(ModelView, model=CategoryModel):
    name_plural = "Category"
    can_export = False
    column_searchable_list = [CategoryModel.name, CategoryModel.active]
    column_list = [CategoryModel.id, CategoryModel.name, CategoryModel.active, CategoryModel.created_at]


class ProductAdmin(ModelView, model=ProductModel):
    name_plural = "Products"
    can_export = False
    column_searchable_list = [ProductModel.name, ProductModel.active]
    column_list = [ProductModel.id, ProductModel.name, ProductModel.sku,
                   ProductModel.category, ProductModel.img, ProductModel.created_at]

    form_ajax_refs = {
        "category": {
            "fields": ("name",),
            "order_by": "id",
        }
    }
