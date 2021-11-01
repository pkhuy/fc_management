from sqlalchemy.sql.expression import null
from database.model import User
from repository.permission_repository import PermissionRepository
from repository.user_group_repository import UserGroupRepository
from repository.user_repository import UserRepository
from repository.permission_repository import PermissionRepository
from flask_login import login_manager
from flask import session
import jwt
import bcrypt
import datetime


class Auth:
    user_repository = UserRepository
    user_group_repository = UserGroupRepository
    permission_repository = PermissionRepository
    def __init__(self, user_repository=UserRepository,
                 permission_repository=PermissionRepository,
                 user_group_repository=UserGroupRepository):
        self.user_repository = user_repository
        self.permission_repository = permission_repository
        self.user_group_repository = user_group_repository

    def check_email_existed(self, email):
        res = self.user_repository.select_by_email(email)
        if res is None:
            return True
        else:
            return False
    
    def register(self, request):
        name = request["name"]
        email = request['email']
        password = request['password']
        
        new_user = self.user_repository.insert_user({"name":name, "email":email, "password":password})
        group_response = self.user_group_repository.insert(new_user["id"], 4) #4 for register user group

        return {"data": new_user}

    def login(self, data):
        user = self.user_repository.select(data)
        if user is not None:
            token = jwt.encode({
                "email": data["email"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                "secretkey",
                algorithm="HS256"
            )
            session["token"] = token
            print(token)
            return user
        return None

    def loaded_user(self, user_id):
        return self.user_repository.loaded_user(user_id)
