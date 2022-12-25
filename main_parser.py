from controllers.book_controller import BookController
from controllers.category_controller import CategoryController
from parser.parser import Parser


if __name__ == '__main__':
    # BookController.clean_dataset()
    BookController.reset_all_table()
    Parser.start()
    BookController.replace_c()
    BookController.finalize()
    CategoryController.finalize()


# print(CategoryController.insert_global_category_and_return("dddddd"))
# for i in CategoryController.get_global_categories():
#     print(i.title)
# print("===============================")
# for i in CategoryController.find_sub_categories_by_global_id(1):
#     print(i.title)
# print("===============================")
# for i in CategoryController.find_book_categories_by_sub_id(1):
#     print(i.title)
# print("===============================")
# for i in BookController.find_books_by_book_category(1):
#     print(i.title)
