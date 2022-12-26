from models.connect import Connect


class CategoryService:
    category_connection: Connect = Connect("CategoryService")

    @staticmethod
    def insert_global(category):
        sql = "INSERT INTO global_category (category_title) VALUES (%s) RETURNING id;"
        CategoryService.category_connection.cursor.execute(sql, (category,))

        CategoryService.category_connection.connection.commit()
        global_id = CategoryService.category_connection.cursor.fetchall()

        return global_id[0][0]

    @staticmethod
    def find_id_by_category_for_global(category):
        category = "\'" + category + "\'"
        sql = """SELECT id FROM global_category WHERE category_title = """ + category
        CategoryService.category_connection.cursor.execute(sql)
        global_category_id = CategoryService.category_connection.cursor.fetchall()

        if not global_category_id:
            return None
        return int(global_category_id[0][0])

    @staticmethod
    def get_global_categories():
        sql = """SELECT * from global_category """
        print(sql)
        CategoryService.category_connection.cursor.execute(sql)

        return CategoryService.category_connection.cursor.fetchall()

    @staticmethod
    def insert_sub(category, global_id):
        sql = "INSERT INTO sub_category (sub_title, global_id) VALUES (%s, %s) RETURNING id;"
        CategoryService.category_connection.cursor.execute(sql, (category, global_id))
        CategoryService.category_connection.connection.commit()

        sub_id = CategoryService.category_connection.cursor.fetchall()
        return sub_id[0][0]

    @staticmethod
    def find_id_by_category_for_sub(category):
        category = "\'" + category + "\'"
        sql = """SELECT id FROM sub_category WHERE sub_title = """ + category
        CategoryService.category_connection.cursor.execute(sql)
        sub_category_id = CategoryService.category_connection.cursor.fetchall()

        if not sub_category_id:
            return None
        return int(sub_category_id[0][0])

    @staticmethod
    def find_book_categories_by_global_id(global_id):
        sql = """SELECT * from sub_category WHERE global_id = %s"""
        CategoryService.category_connection.cursor.execute(sql, (global_id,))

        return CategoryService.category_connection.cursor.fetchall()

    @staticmethod
    def find_id_by_category_for_book(category):
        sql = """SELECT id FROM book_category WHERE category_title = %s"""

        CategoryService.category_connection.cursor.execute(sql, (category,))
        book_category_id = CategoryService.category_connection.cursor.fetchall()

        if not book_category_id:
            return None
        return int(book_category_id[0][0])

    @staticmethod
    def insert_book_category(category, sub_id):
        sql = "INSERT INTO book_category (category_title, sub_id) VALUES (%s, %s) RETURNING id;"""
        CategoryService.category_connection.cursor.execute(sql, (category, sub_id))

        book_category_id = CategoryService.category_connection.cursor.fetchall()
        CategoryService.category_connection.connection.commit()

        return book_category_id[0][0]

    @staticmethod
    def find_book_categories_by_sub_id(sub_id):
        sql = """SELECT * from book_category WHERE sub_id = %s"""
        print(sql)
        CategoryService.category_connection.cursor.execute(sql, (sub_id,))

        return CategoryService.category_connection.cursor.fetchall()

    @staticmethod
    def find_by_id(category_id):
        sql = """SELECT * from book_category WHERE id = %s"""
        print(sql)
        CategoryService.category_connection.cursor.execute(sql, (category_id,))

        return CategoryService.category_connection.cursor.fetchall()[0]

    @staticmethod
    def finalize():
        CategoryService.category_connection.finalize()
