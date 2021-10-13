class GroupPermission():
    def __init__(
        self,
        group_id: int=None,
        permission_id: int=None,
        #user_id: int=None
    ):
        self.group_id = group_id
        self.permission_id = permission_id
        #self.user_id = user_id

    def get_as_json(self):
        return {
            "groupID": self.group_id,
            "permissionID": self.permission_id,
            #"userID": self.user_id
        }