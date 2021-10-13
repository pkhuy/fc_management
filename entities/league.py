class League():
    def __init__(self, id: int, name: str, total_team: int=32): 
        id = id
        name = name
        total_team = total_team
    def __repr__(self):
        return f"League('{self.name}', '{self.number}')"

    def get_as_json(self):
        return {
            "leagueID": self.id,
            "leaguename": self.name,
            "totalteam": self.total_team
        }