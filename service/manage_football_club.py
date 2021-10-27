from repository.football_club_repository import FootballClubRepository
from repository.league_fc_repository import LeagueFCRepository
from repository.league_repository import LeagueRepository
from service.manage_user import ManageUser

#CRUD
class ManageFootballClub:
    football_club_repository = FootballClubRepository()
    league_com_repository = LeagueFCRepository()
    league_repository = LeagueRepository()
    user_service = ManageUser()

    def __init__(self):
        pass

    def read_per(self, data):
        return self.user_service.get_cur_user_permission({
            "current_user_id": data["current_user_id"],
            "entity": "football_club"
        })

    def create(self, data):
        cur_user_per = self.read_per(data)

        if 'POST' in cur_user_per:
            res = self.football_club_repository.insert(data)
            return res
        else:
            return {"res": "u dont have enough permission"}

    def read_all(self):
        res = self.football_club_repository.select_all()
        return res

    def update(self, data):
        cur_user_per = self.read_per(data)

        if 'UPDATE' in cur_user_per:
            res = self.football_club_repository.update(data)
            return res
        else:
            return {"res": "u dont have enough permission"}
            
    def read_by_id(self, id):
        return self.football_club_repository.select_by_id(id)

    def delete(self, data):
        cur_user_per = self.read_per(data)
        if "DELETE" in cur_user_per:
            res = self.football_club_repository.drop_row(id)
            return res
        return {"res": "u dont have enough permission"}

    def add_league_com(self, data):
        check_league = self.league_repository.select_by_id(data["league_id"])
        if check_league is None:
            return "No found", 400
        if check_league["quantity"] == 0:
            return "Max FC join in", 400
        check_league_com = self.league_com_repository.select(data)
        if check_league_com is None:
            self.league_repository.update({
                    "id": data["league_id"], 
                    "name": str(check_league["name"]),
                    "quantity": int(check_league["quantity"]) - 1
                })
            return self.league_com_repository.insert(data)
        return "This FC has already in this league", 400
