from models.connect import Connect
from models.user import User


class UserService:
    user_connection: Connect = Connect("UserService")

    @staticmethod
    def insert(user: User):
        sql = """INSERT INTO users (user_id, username, full_name, role) VALUES (%s, %s, %s, %s)"""
        UserService.user_connection.cursor.execute(sql, (user.user_id, user.username, user.full_name, user.role))
        UserService.user_connection.connection.commit()

    @staticmethod
    def find_user_by_user_id(user_id: int):
        sql = """SELECT * FROM users WHERE user_id = %s"""
        UserService.user_connection.cursor.execute(sql, (user_id,))

        if not UserService.user_connection.cursor.fetchall():
            return False
        return True

    @staticmethod
    def get_users():
        sql = """SELECT * FROM users """
        UserService.user_connection.cursor.execute(sql)
        return UserService.user_connection.cursor.fetchall()

    @staticmethod
    def find_by_id(user_id: int):
        sql = """SELECT * FROM user WHERE id = %s"""
        UserService.user_connection.cursor.execute(sql, (user_id,))
        return UserService.user_connection.cursor.fetchall()[0]

    @staticmethod
    def finalize():
        UserService.user_connection.finalize()

