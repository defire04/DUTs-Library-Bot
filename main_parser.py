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



