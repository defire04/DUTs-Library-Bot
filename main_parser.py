from controllers.parser import Parser
from services.book_service import QueryService

# if __name__ == '__main__':
#     BookService.clean_dataset()
#     Parser.start()
#     BookService.replace_c()
#     BookService.finalize()



print(QueryService.find_books_by_query_id(1))