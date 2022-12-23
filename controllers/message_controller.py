from typing import List
from models.book import Book
from models.user import User
from util.util import string_trim


class MessageController:
    @staticmethod
    def prepare_page_message(page: List[Book]):
        books_strings = []
        for book in page:
            books_strings.append(
                            "-" * 60 + "\n"
                            "<strong>" + string_trim(str(book.title)) + "</strong>\n" +
                            "Id в бд: " + str(book.id) + "\n"
                            "Автор: " + string_trim(str(book.author)) + "\n"
                            "Год публикации: " + str(book.year_of_publication) + "\n"
                            "<a href='" + str(book.link) + "'>Ссылка на книгу</a>")
        return "\n".join(books_strings)

    @staticmethod
    def prepare_page_message_for_users(users: List[User]):
        users_strings = []
        for user in users:
            users_strings.append(
                            "-" * 60 + "\n" 
                            "User id:" + str(user.user_id) + '\n'
                            "Username: " + user.username)

        return "\n".join(users_strings)