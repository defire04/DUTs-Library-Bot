from controllers.book_controller import BookController
from controllers.category_controller import CategoryController
from controllers.sorter_controller import Sorter
from parser.parser import Parser

# if __name__ == '__main__':
#     # BookController.clean_dataset()
#     BookController.reset_all_table()
#     Parser.start()
#     BookController.replace_c()
#     BookController.finalize()
#     CategoryController.finalize()
#


for i in Sorter.sort_by_author(BookController.find_books_by_author("Пашко")):
    print(i.author)
print("______________REVERSE_____________________")

for i in Sorter.sort_by_author_reverse(BookController.find_books_by_author("Пашко")):
    print(i.author)
