from controllers import telegram_bot

# if __name__ == '__main__':
#     telegram_bot.start()
from models.book import Book

b1 = Book("Book")
b1.author = "Author1"
b2 = Book("Book")
b2.author = "Author"
print(b1 == b2)

