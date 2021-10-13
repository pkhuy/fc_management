class Group():
    def __init__(self, id, name):      
        id = id
        name = name
    def __repr__(self):
        return f"Group('{self.name}')"
    def get_as_json(self):
        return {
            "groupID": self.id,
            "groupname": self.name
        }