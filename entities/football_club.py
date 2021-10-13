class FootballClub():
    def __init__(self, id, name, total_player=26):
        
        id = id
        name = name
        total_player = total_player

    def __repr__(self):
        return f"League('{self.name}', '{self.total_player}')"

    def get_as_json(self):
        return {
            "FCID": self.id,
            "FCname": self.name,
            "total_player": self.total_player
        }