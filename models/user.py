class UserRoleEnum:
    ADMIN = "ADMIN"
    USER = "USER"


class User:
    def __init__(self, user_id: int, username: str, full_name: str, role=UserRoleEnum.USER):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.role = role

    @classmethod
    def create(cls, id, user_id, username, full_name, role):
        user = cls(user_id, username, full_name, role)
        user.id = id
        return user


class Admin(User):

    def __init__(self, admin_id: int, admin_username: str, full_name: str):
        super().__init__(admin_id, admin_username, full_name, UserRoleEnum.ADMIN)
