from typing import List
from aiogram import types
from models.user import User, Admin
from services.user_service import UserService
from resources.config import admins

ADMINS = admins


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
    def find_by_id(user_id: int):
        return User(*UserService.find_by_id(user_id)[0])

    @staticmethod
    def add_new_user(user_message: types.Message):
        if not UserController.check_is_user_in_db(user_message.from_user.id):
            if user_message.from_user.id in ADMINS:
                user = Admin(user_message.from_user.id, user_message.from_user.username, user_message.from_user.full_name)
            else:
                user = User(user_message.from_user.id, user_message.from_user.username, user_message.from_user.full_name)
            UserController.insert(user)

    @staticmethod
    def result_to_list(find_result):
        users: List[User] = []

        for user in find_result:
            users.append(User.create(*user))

        return users

    @staticmethod
    def finalize():
        UserService.finalize()
