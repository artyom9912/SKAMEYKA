from flask_login import UserMixin

class User(UserMixin):
    id = None
    userName =  None
    name = None
    relevant = 1
    admin = 0