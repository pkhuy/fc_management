from repository.league_repository import LeagueRepository
from repository.league_fc_repository import LeagueFCRepository
from service.manage_user import ManageUser
#CRUD
class ManageLeague:
    league_repository = LeagueRepository()
    league_fc_repository = LeagueFCRepository()
    user_service = ManageUser()

    def __init__(self):
        pass

    def read_per(self, data):
        return self.user_service.get_cur_user_permission({
            "current_user_id": data["current_user_id"],
            "entity": "league"
        })

    def create(self, data):
        cur_user_per = self.read_per(data)

        if 'create' in cur_user_per:
            res = self.league_repository.insert(data)
            return res
        else:
            return {"res": "u dont have enough permission"}

    def read_all(self):
        res = self.league_repository.select_all()
        return res

    def update(self, data):
        cur_user_per = self.read_per(data)

        if 'change' in cur_user_per:
            res = self.league_repository.update(data)
            return res
        else:
            return {"res": "u dont have enough permission"}

    def read_by_id(self, id):
        return self.league_repository.select_by_id(id)

    def delete(self, data):
        cur_user_per = self.read_per(data)
        if 'delete' in cur_user_per:
            self.league_fc_repository.drop_row(data["id"])
            res = self.league_repository.drop_row(data["id"])
            return res
        return {"res": "u dont have enough permission"}
