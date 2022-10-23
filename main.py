from controllers import Parser

url = 'https://www.dut.edu.ua/ua/lib/1/category/2122'
# Parser.start(url)
# print(Parser.get_list_of_links_to_books_by_section("https://www.dut.edu.ua/ua/lib/1/category/2264"))
for i in Parser.get_links_to_sections_within_section("https://www.dut.edu.ua/ua/lib/1/category/2141"):
    print(i)

# from models import Book
#
# b = Book("Сережа")
# b.new = 12
# print("Я птица. Меня зовут " + b.title)
# print(b.new)