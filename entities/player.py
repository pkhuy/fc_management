class Player:
    def __init__(self, id, name,position,  fc_id):
        self.id = id
        self.name = name
        self.position = position
        self.fc_id = fc_id

    def __repr__(self):
        
        return f"League('{self.name}', '{self.position}')"

    def get_as_json(self):
        return {
                "id": self.id,
                "name": self.name,
                "position": self.position,
                "fc_id": self.fc_id
            }