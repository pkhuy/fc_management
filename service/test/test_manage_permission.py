from repository.permission_repository import PermissionRepository
from repository.user_permission_repository import UserPermissionRepository

class ManagePermission:
    permission_repository = PermissionRepository()
    user_permission_repository = UserPermissionRepository()

    def __init__(self):
        pass

    def create(delf, data):
        pass

    def read_all(self):
        res = self.permission_repository.select_all()
        return res

    def read_by_id(self, id):
        return self.permission_repository.select_by_id(id)

    def update(self, data):
        pass

    def delete(self, data):
        pass