class UserGroup():
    def __init__(self, user_id: int, group_id: int):
        user_id = user_id,
        group_id = group_id



    def get_as_json(self):
        return {
            "userID": self.user_id,
            "groupId": self.group_id
        }
