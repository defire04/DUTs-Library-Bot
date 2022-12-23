from services.user_service import UserService


class UserController:
    @staticmethod
    def insert(user):
        UserService.insert(user)

    @staticmethod
    def check_is_user_in_db(user_id):
        return UserService.find_user_by_user_id(user_id)