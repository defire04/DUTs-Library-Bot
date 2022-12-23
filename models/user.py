class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    @classmethod
    def create(cls, id, user_id, username):
        user = cls(user_id, username)
        user.id = id
        return user
