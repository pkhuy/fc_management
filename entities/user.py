from datetime import date, datetime
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

class User():
    def __init__(
        self,
        id: int=None,
        name: str=None,
        email: str=None,
        password: str=None,
        created_at: datetime=None,
        last_login: datetime=None,
        group_id: int=None,
        permission_id: int=None,
    ):
        id = id
        name = name
        email = email
        __password = password
        created_at = created_at
        last_login = last_login
        group_id = group_id
        permission_id = permission_id
        
    def __repr__(self) -> str:
        pass

    def get_as_json(self):
        return {
            "userID": self.id,
            "username": self.name,
            "email": self.email,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "group_id": self.group_id,
            "permission_id": self.permission_id
        }

