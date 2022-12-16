from typing import List

import psycopg2

from models.book import Book
from models.query import Query
from resources.config import host, username, password, datasource
from services.book_service import BookService


class QueryService:
    connection = psycopg2.connect(host=host, user=username, password=password, database=datasource)
    cursor = connection.cursor()

    @staticmethod
    def create(sql: str, books: List[Book]):
        string_books_id = []

        for book in books:
            string_books_id.append(str(book.id))

        return QueryService.insert(sql, " ".join(string_books_id))

    @staticmethod
    def insert(search_string, string_books_id):
        sql = """INSERT INTO query(search_string, string_books_id) VALUES (%s, %s);"""
        print(sql)
        record_to_insert = (search_string, string_books_id)
        QueryService.cursor.execute(sql, record_to_insert)

        sql = """SELECT currval(pg_get_serial_sequence('query','id'));"""
        QueryService.cursor.execute(sql)
        QueryService.connection.commit()
        tuple_insert_id = QueryService.cursor.fetchall()

        return tuple_insert_id[0][0]

    @staticmethod
    def find_by_id(id):

        sql = "SELECT * FROM query WHERE id = " + str(id)
        print(sql)
        QueryService.cursor.execute(sql)
        tuple_query = QueryService.cursor.fetchall()
        query = Query(*tuple_query[0])

        return query

    @staticmethod
    def find_books_by_query_id(query_id):
        sql = "SELECT * FROM query WHERE id = " + str(query_id)
        QueryService.cursor.execute(sql)
        tuple_query = QueryService.cursor.fetchall()
        query = Query(*tuple_query[0])

        return BookService.find_book_by_ids(query.string_books_id)


    @staticmethod
    def finalize():
        QueryService.cursor.close()
        QueryService.connection.close()
        print("Database connection dead! ------------------ Query")
