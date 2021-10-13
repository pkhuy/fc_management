class Player():
    def __init__(self, id: int=None, name: str=None,position: str=None,  fc_id: int=None):
        id = id,
        name = name
        position = position
        fc_id = fc_id

    def __repr__(self):
        return f"League('{self.name}', '{self.number}')"

    def get_as_json(self):
        return {
            "playerID": self.id,
            "playername": self.name,
            "playerPosition": self.position,
            "fcID_of_player": self.fc_id
        }