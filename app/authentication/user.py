from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, user_ik):
        if user_id and user_ik:
            self.user_id = user_id
            self.user_ik = user_ik
        else:
            raise ValueError("No user_id or user_ik found in session")
