class UserPermission():
    def __init__(self, id, user_id, permission_id):
        self.id = id
        self.user_id = user_id
        self.permission_id = permission_id

    def get_as_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "permission_id": self.permission_id
        }
