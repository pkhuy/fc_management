class LeagueFC:
    def __init__(self, id: int, league_id: int, fc_id: int):
        self.id = id
        self.league_id = league_id
        self.fc_id = fc_id

    def __repr__(self):
        return f"League('{self.id}', '{self.league_id}', '{self.fc_id}')"

    def get_as_json(self):
        return {
                "id": self.id,
                "league_id": self.league_id,
                "fc_id": self.fc_id
            }
