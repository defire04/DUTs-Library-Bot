from typing import List

import psycopg2

from models.category import Category
from resources.config import host, username, password, datasource


class CategoryService:
    connection = psycopg2.connect(host=host, user=username, password=password, database=datasource)
    cursor = connection.cursor()

    @staticmethod
    def insert_global(category):
        sql = "INSERT INTO global_category (category_title) values ('" + category + "');"
        CategoryService.cursor.execute(sql)

        sql = """SELECT currval(pg_get_serial_sequence('global_category','id'));"""
        CategoryService.cursor.execute(sql)

        CategoryService.connection.commit()
        global_id = CategoryService.cursor.fetchall()

        return global_id[0][0]

    @staticmethod
    def find_id_by_category_for_global(category):
        category = "\'" + category + "\'"
        sql = """SELECT id FROM global_category WHERE category_title = """ + category

        CategoryService.cursor.execute(sql)
        global_category_id = CategoryService.cursor.fetchall()

        if not global_category_id:
            return None
        return int(global_category_id[0][0])

    @staticmethod
    def insert_sub(category, global_id):
        sql = "INSERT INTO sub_category (sub_title, global_id) VALUES (%s, %s);"

        record_to_insert = (category, global_id)
        CategoryService.cursor.execute(sql, record_to_insert)
        CategoryService.connection.commit()

        sql = """SELECT currval(pg_get_serial_sequence('sub_category','id'));"""
        CategoryService.cursor.execute(sql)

        sub_id = CategoryService.cursor.fetchall()
        return sub_id[0][0]

    @staticmethod
    def find_id_by_category_for_sub(category):
        category = "\'" + category + "\'"
        sql = """SELECT id FROM sub_category WHERE sub_title = """ + category

        CategoryService.cursor.execute(sql)
        sub_category_id = CategoryService.cursor.fetchall()

        if not sub_category_id:
            return None
        return int(sub_category_id[0][0])

    @staticmethod
    def get_global_categories():
        sql = """SELECT * from global_category """
        print(sql)
        CategoryService.cursor.execute(sql)

        return CategoryService.cursor.fetchall()

    @staticmethod
    def find_id_by_category_for_book(category: str):

        sql = """SELECT id FROM book_category WHERE category_title = %s"""

        CategoryService.cursor.execute(sql, (category,))
        book_category_id = CategoryService.cursor.fetchall()

        if not book_category_id:
            return None
        return int(book_category_id[0][0])

    @staticmethod
    def insert_book_category(category):
        sql = "INSERT INTO book_category (category_title) VALUES (%s) RETURNING id;"""
        CategoryService.cursor.execute(sql, (category,))

        book_category_id = CategoryService.cursor.fetchall()
        CategoryService.connection.commit()

        return book_category_id[0][0]

    @staticmethod
    def finalize():
        CategoryService.cursor.close()
        CategoryService.connection.close()
        print("Database connection dead! ------------------ Category")




