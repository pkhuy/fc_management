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
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.last_login = last_login
        self.group_id = group_id
        self.permission_id = permission_id
        
    def __repr__(self) -> str:
        pass

    def get_as_json(self):
        return {
                "id": self.id,
                "name": self.name,
                "email": self.email,
            }
            #"created_at": self.created_at,
            #"last_login": self.last_login,
            #"group_id": self.group_id,
            #"permission_id": self.permission_id


