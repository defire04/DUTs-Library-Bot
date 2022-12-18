from services.category_service import CategoryService


class CategoryController:

    @staticmethod
    def insert_global_category_and_return(category):
        global_category_id = CategoryService.find_id_by_category_for_global(category)

        if global_category_id is None:
            global_category_id = CategoryService.insert_global(category)

        return global_category_id


    @staticmethod
    def insert_sub_category_and_return(sub_category, global_id):
        sub_category_id = CategoryService.find_id_by_category_for_sub(sub_category)

        if sub_category_id is None:
            sub_category_id = CategoryService.insert_sub(sub_category, global_id)

        return sub_category_id


    @staticmethod
    def finalize():
        CategoryService.finalize()
