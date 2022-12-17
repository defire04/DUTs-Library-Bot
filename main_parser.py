from controllers.category_controller import CategoryController
from controllers.parser import Parser
from services.book_service import BookService

if __name__ == '__main__':
    BookService.clean_dataset()
    Parser.start()
    BookService.replace_c()
    BookService.finalize()
    CategoryController.finalize()




