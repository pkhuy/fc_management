from .interface import UserRepositoryInterface, UserInterface
import sqlite3
import traceback


class User(UserInterface):
    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        password: str,
        group_id: int,              #chuc vu
        permission_id: int,         #quyen han
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.group_id = group_id
        self.permission_id = permission_id
