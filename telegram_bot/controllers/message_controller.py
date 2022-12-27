from typing import List
from models.book import Book
from models.user import User
from util.util import string_trim


class MessageController:
    @staticmethod
    def prepare_page_message(page: List[Book], current_page: int, total_pages: int):
        books_strings = ["За Вашим запитом ми знайшли такі книги:  "]
        pages_string = """📄 Сторінка: <strong>{current_page}</strong> з <strong>{total_pages}</strong>""".format(
            current_page=str(current_page),
            total_pages=str(total_pages)
        )
        
        for book in page:
            books_strings.append(
                "📖<strong>" + string_trim(str(book.title)) + "</strong>\n" +
                "👴Автор: " + string_trim(str(book.author)) + "\n"
                 "📅Рік публікації: " + str(book.year_of_publication) + "\n"
                 "🧷<a href='" + str(book.link) + "'>Посилання на книгу</a>")

        books_strings.append(pages_string)

        return ('\n' + "-" * 60 + "\n").join(books_strings)

    @staticmethod
    def prepare_page_message_for_users(users: List[User]):
        users_strings = []
        for user in users:
            users_strings.append(
                "User id:" + str(user.user_id) + '\n'
                "Username: " + str(user.username))

        return ('\n' + "-" * 60 + "\n").join(users_strings)
