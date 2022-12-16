from typing import List
import psycopg2

from models.query import Query
from resources.config import host, username, password, datasource
from models.book import Book
from services.query_servise import QueryService


class BookService:
    connection = psycopg2.connect(host=host, user=username, password=password, database=datasource)
    cursor = connection.cursor()

    @staticmethod
    def insert(book):
        sql = """INSERT INTO books (title, author, lang, document_size, year_of_publication, publishing_house, 
        country, number_of_pages, availability_in_the_library, availability_in_electronic_form, added, 
        classification, document_type, link_to_book) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        record_to_insert = (
            book.title, book.author, book.lang, book.document_size, book.year_of_publication, book.publishing_house,
            book.country, book.number_of_pages, book.availability_in_the_library, book.availability_in_electronic_form,
            book.added, book.classification, book.document_type, book.link)
        BookService.cursor.execute(sql, record_to_insert)
        BookService.connection.commit()

        
    @staticmethod
    def find_by_title_and_create_query(title):
        books = BookService.find_by_title(title)
        query_id = QueryService.create(title, books)
        return {
            "books": books,
            "query_id": query_id
        }

    @staticmethod
    def find_by_title(title):
        like_title = """ '%""" + title + """%';"""
        sql = """SELECT * FROM books WHERE LOWER(title) LIKE""" + like_title.lower()

        print(sql)
        BookService.cursor.execute(sql)
        books: List[Book] = []

        for book in BookService.cursor.fetchall():
            books.append(Book.create_book(*book))

        print("Count of books by request: " + str(len(books)))

        return books

    @staticmethod
    def find_book_by_ids(request_books: str):
        request_books = request_books.replace(" ", ", ")
        sql = """SELECT * FROM books WHERE id in ("""+ request_books +""")"""
        BookService.cursor.execute(sql)

        return BookService.result_to_list(BookService.cursor.fetchall())

    @staticmethod
    def result_to_list(find_result):
        books: List[Book] = []

        for book in find_result:
            books.append(Book.create_book(*book))

        return books

    @staticmethod
    def replace_c():
        sql_select = """UPDATE books SET title = REPLACE(title ,'С++', 'C++' ) WHERE title LIKE '%С++%';
                        UPDATE books SET title = REPLACE(title ,'С#', 'C#' ) WHERE title LIKE '%С#%';"""
        BookService.cursor.execute(sql_select)
        BookService.connection.commit()

    @staticmethod
    def clean_dataset():
        sql_drop = "TRUNCATE TABLE books;"
        BookService.cursor.execute(sql_drop)
        BookService.connection.commit()

    @staticmethod
    def finalize():
        BookService.cursor.close()
        BookService.connection.close()
        print("Database connection dead!")
