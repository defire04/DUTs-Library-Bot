from typing import List

import psycopg2

from models.book import Book
from models.query import Query
from resources.config import host, username, password, datasource


class QueryService:
    connection = psycopg2.connect(host=host, user=username, password=password, database=datasource)
    cursor = connection.cursor()

    @staticmethod
    def insert(search_string, string_books_id):
        sql = """INSERT INTO query(search_string, string_books_id) VALUES (%s, %s) RETURNING id;"""
        print(sql)
        QueryService.cursor.execute(sql, (search_string, string_books_id))

        QueryService.connection.commit()
        tuple_insert_id = QueryService.cursor.fetchall()

        return tuple_insert_id[0][0]

    @staticmethod
    def find_by_id(id):
        sql = "SELECT * FROM query WHERE id = %s "
        print(sql)
        QueryService.cursor.execute(sql, (id, ))
        tuple_query = QueryService.cursor.fetchall()
        query = Query(*tuple_query[0])

        return query

    @staticmethod
    def find_by_search_string(search_string):
        sql = "SELECT id FROM query WHERE search_string = %s "
        print(sql)
        QueryService.cursor.execute(sql, (search_string, ))

        query_id = QueryService.cursor.fetchall()
        if not query_id:
            return None

        return query_id[0][0]

    @staticmethod
    def finalize():
        QueryService.cursor.close()
        QueryService.connection.close()
        print("Database connection dead! ------------------ Query")
