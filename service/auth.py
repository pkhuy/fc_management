from database.model import User
from repository.permission_repository import PermissionRepository
from repository.repository import UserRepository
from repository.permission_repository import PermissionRepository
from flask_login import login_manager
class Auth:
    user_repository = UserRepository()
    permission_repository = PermissionRepository()

    def __init__(self):
        pass

    def register(self, request):
        email = request['email']
        password = request['password']

        response = None
        validate_entry = isinstance(email, str)

        if validate_entry:
            response = self.user_repository.insert_user(email=email, password=password)
        
        return {"success": validate_entry, "data": response}

    def login(self, request):
        email = request['email']
        password  = request['password']
        
        response = None
        validate_entry = isinstance(email, str)
        
        if validate_entry:
            response = self.user_repository.select_user(email=email, password=password)

        return {"success": validate_entry, "data": response}

    def insert_user_permission(self, request):
        name = request['name']
        entity = request['entity']

        response = None
        validate_entry = isinstance(name, str)

        if validate_entry:
            response = self.permission_repository.insert_user_permission(name, entity)

        return {"success": validate_entry, "data": response}

    def get_user_permission(self, request):
        user = request
        entity = 'users'
        response = None

        response = self.permission_repository.select_permission(user, entity)
        return response

    def loaded_user(self, user_id):
        return self.user_repository.loaded_user(user_id)
