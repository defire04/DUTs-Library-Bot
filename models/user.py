class User:
    def __init__(self, user_id, username, full_name):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name

    @classmethod
    def create(cls, id, user_id, username, full_name):
        user = cls(user_id, username, full_name)
        user.id = id
        return user
