import psycopg2

from models.user import User
from resources.config import host, username, password, datasource


class UserService:
    connection = psycopg2.connect(host=host, user=username, password=password, database=datasource)
    cursor = connection.cursor()

    @staticmethod
    def insert(user: User):
        sql = """INSERT INTO users (user_id, username) VALUES (%s, %s)"""
        UserService.cursor.execute(sql, (user.user_id, user.username))
        UserService.connection.commit()

    @staticmethod
    def finalize():
        UserService.cursor.close()
        UserService.connection.close()
        print("Database connection dead!")

    @staticmethod
    def find_user_by_user_id(user_id: int):
        sql = """SELECT * FROM users WHERE user_id = %s"""
        UserService.cursor.execute(sql, (user_id,))

        if not UserService.cursor.fetchall():
            return False
        return True
