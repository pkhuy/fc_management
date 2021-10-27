from repository.group_repository import GroupRepository
from repository.user_group_repository import UserGroupRepository

class ManageGroup:
    group_repository = GroupRepository()
    user_group_repository = UserGroupRepository()
    def __init__(self):
        pass

    def create(self, data):
        pass

    def read_all(self):
        res = self.group_repository.get_all()
        return res

    def read_by_id(self, id):
        return self.group_repository.select_by_id(id)

    def read_by_user_id(self, user_id):
        return self.user_group_repository.select_user_group(user_id=user_id)

    def update(self, data):
        pass

    def delete(self, data):
        cur_user_per = 'admin'