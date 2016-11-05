from flask_login import UserMixin


class User(UserMixin):
    # proxy for a database of users
    user_database = {"Admin": ("Admin", "horse_staple")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls, id):  # pylint: disable=redefined-builtin
        return cls.user_database.get(id)