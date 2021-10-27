class UserGroup():
    def __init__(self, id: int, user_id: int, group_id: int):
        self.id = id
        self.user_id = user_id,
        self.group_id = group_id



    def get_as_json(self):
        return {
            "id": self.id,
            "userID": self.user_id,
            "groupId": self.group_id
        }
