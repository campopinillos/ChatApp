from werkzeug.security import check_password_hash


class User:
    def __init__(self, user, email, password):
        self.user = user
        self.email = email
        self.password = password

    @staticmethod
    def is_authenticated(self):
        return True

    @staticmethod
    def is_active(self):
        return True

    @staticmethod
    def is_anonymous(self):
        return True

    def get_id(self):
        return self.user

    def unhash_password(self, password_input):
        return check_password_hash(self.password, password_input)
