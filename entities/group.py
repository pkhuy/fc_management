class Group():
    def __init__(self, id, name):      
        self.id = id
        self.name = name
    def __repr__(self):
        return f"Group('{self.name}')"
    def get_as_json(self):
        return {
                "id": self.id,
                "name": self.name
            }
