from typing import List
from aiogram import types
from models.user import User
from services.user_service import UserService


class UserController:
    @staticmethod
    def insert(user):
        UserService.insert(user)

    @staticmethod
    def check_is_user_in_db(user_id):
        return UserService.find_user_by_user_id(user_id)

    @staticmethod
    def get_users():
        return UserController.result_to_list(UserService.get_users())

    @staticmethod
    def result_to_list(find_result):
        users: List[User] = []

        for user in find_result:
            users.append(User.create(*user))

        return users

    @staticmethod
    def add_new_user(user_message: types.Message):

        if not UserController.check_is_user_in_db(user_message.from_user.id):
            user = User(user_message.from_user.id, user_message.from_user.username, user_message.from_user.full_name)
            UserController.insert(user)

    @staticmethod
    def finalize():
        UserService.finalize()

