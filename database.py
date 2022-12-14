from typing import List
import psycopg2
from config import host, username, password, datasource
from models import Book


class SearchResult:
    def __init__(self, books: List[Book], search_query: str):
        self.data = books
        self.search_query = search_query
        self.data_length = len(books)


class PagesResult:
    def __init__(self, result: SearchResult, results_per_page: int = 4):
        self.result = result
        self.results_per_page = results_per_page

    def get_page(self, index: int):
        page = self.result.data[index * self.results_per_page: (index + 1) * self.results_per_page]
        return page


class DatabaseConnect:
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
            book.added, book.classification, book.document_type, book.link_to_book)
        DatabaseConnect.cursor.execute(sql, record_to_insert)
        DatabaseConnect.connection.commit()

    @staticmethod
    def find_by_title(title):
        like_title = """ '%""" + title + """%';"""
        sql = """SELECT * FROM books WHERE title LIKE""" + like_title

        print(sql)
        DatabaseConnect.cursor.execute(sql)
        books: List[Book] = []

        for book in DatabaseConnect.cursor.fetchall():
            books.append(Book(book[0], book[1], book[2], book[3], book[4], book[5], book[6],
                              book[7], book[8], book[9], book[10], book[11], book[12], book[13], book[14]))

        print(len(books))
        return books

    @staticmethod
    def finalize():
        DatabaseConnect.cursor.close()
        DatabaseConnect.connection.close()
        print("Database connection dead!")
