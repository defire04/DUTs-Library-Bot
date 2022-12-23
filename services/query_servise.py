from models.connect import Connect
from models.query import Query


class QueryService:
    query_connection: Connect = Connect("QueryService")

    @staticmethod
    def insert(search_string, string_books_id):
        sql = """INSERT INTO query(search_string, string_books_id) VALUES (%s, %s) RETURNING id;"""
        print(sql)
        QueryService.query_connection.cursor.execute(sql, (search_string, string_books_id))

        QueryService.query_connection.connection.commit()
        tuple_insert_id = QueryService.query_connection.cursor.fetchall()

        return tuple_insert_id[0][0]

    @staticmethod
    def find_by_id(id):
        sql = "SELECT * FROM query WHERE id = %s "
        print(sql)
        QueryService.query_connection.cursor.execute(sql, (id, ))
        tuple_query = QueryService.query_connection.cursor.fetchall()
        query = Query(*tuple_query[0])

        return query

    @staticmethod
    def find_by_search_string(search_string):
        sql = "SELECT id FROM query WHERE search_string = %s "
        print(sql)
        QueryService.query_connection.cursor.execute(sql, (search_string, ))

        query_id = QueryService.query_connection.cursor.fetchall()
        if not query_id:
            return None

        return query_id[0][0]

    @staticmethod
    def finalize():
        QueryService.query_connection.finalize()
