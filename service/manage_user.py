from repository.user_repository import UserRepository
from repository.user_group_repository import UserGroupRepository
from repository.user_permission_repository import UserPermissionRepository


class ManageUser:
    user_repository = UserRepository
    user_group_repository = UserGroupRepository
    user_permission_repository = UserPermissionRepository

    def __init__(self, user_repository=UserRepository,
                 user_permission_repository=UserPermissionRepository,
                 user_group_repository=UserGroupRepository):
        self.user_repository = user_repository
        self.permission_repository = user_permission_repository
        self.user_group_repository = user_group_repository


    def read_all(self):
        res = self.user_repository.select_all()
        return res

    def read_by_id(self, id):
        return self.user_repository.select_by_id(id)

    def update(self, req):
        cur_user_group = self.user_group_repository.select_user_group(
            int(req["current_user_id"]))
        if 'admin' in cur_user_group:
            res = self.user_repository.update(req)
            return res
        if 'manager' in cur_user_group:
            user_managed_group = self.user_group_repository.select_user_group(
                req["id"]
            )
            print(user_managed_group)
            if 'admin' in user_managed_group or 'manager' in user_managed_group:
                return {"res": "u dont have enough permission"}
            else:
                res = self.user_repository.update(req)
                return res

        return {"res": "u dont have enough permission"}

    def get_cur_user_permission(self, req):
        user_id = req["current_user_id"]
        entity = req["entity"]
        response = None

        response = self.user_permission_repository.select_permission_entity(
            user_id, entity)
        return response

    def loaded_user(self, user_id):
        return self.user_repository.loaded_user(user_id)

    
    def delete(self, data):
        cur_user_per = self.get_cur_user_permission(data)
        if 'DELETE' in cur_user_per:
            res = self.user_repository.drop_row(data["id"])
            self.user_group_repository.drop_row(data["id"])
            self.user_permission_repository.drop_row(data["id"])
            return res
        return {"res": "u dont have enough permission"}

    def get_group_by_user_id(self, user_id):
        return self.user_group_repository.select_user_group(user_id=user_id)
