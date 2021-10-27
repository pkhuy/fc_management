from repository.player_repository import PlayerRepository
from service.manage_user import ManageUser
from repository.football_club_repository import FootballClubRepository

class ManagePlayer:
    player_repository = PlayerRepository()
    user_service = ManageUser()
    fc_repository = FootballClubRepository()

    def __init__(self):
        pass

    def read_per(self, data):
        return self.user_service.get_cur_user_permission({
            "current_user_id": data["current_user_id"],
            "entity": "player"
        })

    def create(self, data):
        cur_user_per = self.read_per(data)
        join_fc = self.fc_repository.select_by_id(data["fc_id"])
        if 'POST' in cur_user_per:
            if join_fc is None:
                return "No found this fc", 400
            if join_fc["quantity"] == 0:
                return "Max player join in", 400
            print(join_fc["quantity"]-1)
            self.fc_repository.update({
                "current_user_id": data["current_user_id"],
                "id": int(join_fc["id"]),
                "name": str(join_fc["name"]),
                "quantity": int(join_fc["quantity"]-1)
            })
            res = self.player_repository.insert(data)
            return res
        return {"res": "u dont have enough permission"}

    def read_all(self):
        res = self.player_repository.select_all()
        return res

    def read_by_id(self, id):
        return self.player_repository.select_by_id(id)

    def update(self, data):
        cur_user_per = self.read_per(data)

        if 'UPDATE' in cur_user_per:
            res = self.player_repository.update(data)
            return res
        else:
            return {"res": "u dont have enough permission"}   

    def delete(self, data):
        cur_user_per = self.read_per(data)
        if 'DELETE' in cur_user_per:
            out_player = self.read_by_id(id)
            out_fc = self.fc_repository.select_by_id(out_player["fc_id"])
            self.fc_repository.update({
                "id": out_fc["id"],
                "name": str(out_fc["name"]),
                "quantity": int(out_fc["quantity"]+1)
            })
            res = self.player_repository.drop_row(id)
            return res
        return {"res": "u dont have enough permission"}