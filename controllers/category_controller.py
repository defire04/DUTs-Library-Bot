from typing import List

from models.category import Category
from services.category_service import CategoryService


class CategoryController:

    @staticmethod
    def insert_global_category_and_return(category):
        global_category_id = CategoryService.find_id_by_category_for_global(category)

        if global_category_id is None:
            global_category_id = CategoryService.insert_global(category)

        return global_category_id

    @staticmethod
    def get_global_categories():
        categories: List[Category] = []

        for category in CategoryService.get_global_categories():
            categories.append(Category(*category))

        return categories

    @staticmethod
    def insert_sub_category_and_return(sub_category, global_id):
        sub_category_id = CategoryService.find_id_by_category_for_sub(sub_category)

        if sub_category_id is None:
            sub_category_id = CategoryService.insert_sub(sub_category, global_id)

        return sub_category_id

    @staticmethod
    def find_sub_categories_by_global_id(global_id):
        categories: List[Category] = []

        for category in CategoryService.find_book_categories_by_sub_id(global_id):
            categories.append(Category(category[0], category[1]))

        return categories

    @staticmethod
    def insert_book_category_and_return(category, sub_id):
        book_category_id = CategoryService.find_id_by_category_for_book(category)
        if book_category_id is None:
            book_category_id = CategoryService.insert_book_category(category, sub_id)

        return book_category_id

    @staticmethod
    def find_book_categories_by_sub_id(sub_id):
        categories: List[Category] = []

        for category in CategoryService.find_book_categories_by_sub_id(sub_id):
            categories.append(Category(category[0], category[1]))

        return categories


    @staticmethod
    def finalize():
        CategoryService.finalize()
