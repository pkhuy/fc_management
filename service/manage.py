from database.model import User
from repository.permission_repository import PermissionRepository
from repository.repository import UserRepository
from repository.group_repository import GroupRepository
from repository.permission_repository import PermissionRepository
from repository.player_repository import PlayerRepository
from flask_login import login_manager


class Manage:
    user_repository = UserRepository()
    permission_repository = PermissionRepository()
    group_repository = GroupRepository()
    player_repository = PlayerRepository()
    def __init__(self):
        pass

    def get_all_user(self):
        res = self.user_repository.select_all_user()
        return res

    def get_all_player(self):
        res = self.player_repository.get_all_player()
        return res

    def get_user_group(self, request):
        user_id = request['userID']
        response = self.group_repository.select_user_group(user_id)

    def insert_user_permission(self, request):
        name = request['name']
        entity = request['entity']

        response = None
        validate_entry = isinstance(name, str)

        if validate_entry:
            response = self.permission_repository.insert_user_permission(
                name, entity)

        return {"success": validate_entry, "data": response}

    def get_user_permission(self, request):
        user = request["current_user"]
        entity = request["entity"]
        response = None

        response = self.permission_repository.select_permission(user, entity)
        return response

    def loaded_user(self, user_id):
        return self.user_repository.loaded_user(user_id)
