from controllers.parser import Parser
from services.book_service import BookService

if __name__ == '__main__':
    BookService.clean_dataset()
    Parser.start()
    BookService.replace_C()
    BookService.finalize()
