from repository.user_repository import UserRepository
from repository.user_permission_repository import UserPermissionRepository
from repository.permission_repository import PermissionRepository
from repository.user_group_repository import UserGroupRepository


class UserPermissionService:
    user_repository = UserRepository
    user_permission_repository = UserPermissionRepository
    permission_repository = PermissionRepository
    user_group_repository = UserGroupRepository

    def __init__(self, user_repository=UserRepository,
                 user_permission_repository=UserPermissionRepository,
                 permission_repository=PermissionRepository, 
                 user_group_repository=UserGroupRepository):
        self.user_repository = user_repository
        self.user_permission_repository = user_permission_repository
        self.permission_repository = permission_repository
        self.user_group_repository = user_group_repository

    def create(self, data):
        sv_data = {
            "user_id": data["user_id"],
            "permission_id": data["permission_id"]
        }
        check_exist = self.user_permission_repository.select(sv_data)
        if check_exist is None:
            cur_user_group = self.user_group_repository.select_user_group(
                data["current_user_id"]
            )
            if 'admin' in cur_user_group:
                res = self.user_permission_repository.insert(sv_data)
                return res
            if 'manager' in cur_user_group:
                user_managed_group = self.user_group_repository.select_user_group(
                    sv_data["user_id"]
                )
                if 'admin' in user_managed_group or 'manager' in user_managed_group:
                    return {"res": "u dont have enough permission"}
                else:
                    res = self.user_permission_repository.insert(sv_data)
                    return res

            return {"res": "u dont have enough permission"}
        return {"res": "this user had had this permission", "response code": 200}

    def read_all(self):
        return self.user_permission_repository.select_all()

    def read_by_id(self, user_id, permission_id):
        return self.user_permission_repository.select_by_id(user_id, permission_id)

    def read_by_user_id(self, user_id):
        return self.user_permission_repository.select_by_user_id(user_id)

    #not use
    def update(self, req):
        cur_user_group = self.user_group_repository.select_user_group(
            int(req["current_user_id"]))
        if 'admin' in cur_user_group:
            res = self.user_permission_repository.update(req)
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

    def delete(self, data):
        check_exist = self.user_permission_repository.select(data)
        if check_exist is None:
            return {"Notthing to delete"}
        cur_user_group = self.user_group_repository.select_user_group(
            int(data["current_user_id"]))
        if 'admin' in cur_user_group:
            res = self.user_permission_repository.drop_row_by_id(check_exist["id"])
            return res
        if 'manager' in cur_user_group:
            user_managed_group = self.user_group_repository.select_user_group(
                data["user_id"]
            )
            print(user_managed_group)
            if 'admin' in user_managed_group or 'manager' in user_managed_group:
                return {"res": "u dont have enough permission"}
            else:
                return self.user_permission_repository.drop_row_by_id(
                    check_exist["id"])

        return "u dont have enough permission", 405

    def get_group_by_user_id(self, user_id):
        return self.user_group_repository.select_user_group(user_id=user_id)
