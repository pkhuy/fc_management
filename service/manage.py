from database.model import User, UserGroup
from repository.permission_repository import PermissionRepository
from repository.user_repository import UserRepository
from repository.group_repository import GroupRepository
from repository.player_repository import PlayerRepository
from repository.football_club_repository import FootballClubRepository
from repository.league_repository import LeagueRepository
from repository.user_group_repository import UserGroupRepository
from repository.user_permission_repository import UserPermissionRepository
from flask_login import login_manager


class Manage:
    user_repository = UserRepository
    permission_repository = PermissionRepository()
    group_repository = GroupRepository()
    player_repository = PlayerRepository()
    football_club_repository = FootballClubRepository()
    league_repository = LeagueRepository()
    user_group_repository = UserGroupRepository()
    user_permission_repository = UserPermissionRepository()
    def __init__(self):
        pass

    def get_all_user(self):
        res = self.user_repository.select_all()
        return res

    def get_all_permission(self):
        res = self.permission_repository.select_all()
        return res

    def get_all_group(self):
        res = self.group_repository.get_all()
        return res

    def get_all_player(self):
        res = self.player_repository.select_all()
        return res

    def get_all_football_club(self):
        res = self.football_club_repository.select_all()
        return res

    def get_all_league(self):
        res = self.league_repository.select_all()
        return res

    def update_player(self, data):
        cur_user_per = Manage().get_cur_user_permission({
            "user_id": data["current_user_id"],
            "entity": "player"
        })
        cur_user_group = self.user_group_repository.select_user_group(
            int(data["current_user_id"]))
        
        if 'UPDATE' in cur_user_per:
            res = self.player_repository.update(data)
            return res
        else:
            return {"res": "u dont have enough permission"}


    def update_user(self, req):
        cur_user_group = self.user_group_repository.select_user_group(
            int(req["current_user_id"]))
        if 'admin' in cur_user_group:
            res = self.user_repository.update(req["data"])
            return res
        else:
            if 'manager' in cur_user_group:
                user_managed_group = self.user_group_repository.select_user_group(
                    req["data"]["id"]
                )
                print(user_managed_group)
                if 'admin' in user_managed_group or 'manager' in user_managed_group:
                    return {"res": "u dont have enough permission"}
                else:
                    res = self.user_repository.update(req["data"])
                    return res
            
            else:
                return {"res": "u dont have enough permission"}
    
    def update_football_club(self, req):
        res = self.football_club_repository.update(req)
        return res

    def create_player(self, req):
        res = self.player_repository.insert(req)
        return res

    def insert_user_permission(self, request):
        permission_id = self.permission_repository.select(
            {
                "permission_name": request["permission"],
                "entity": request["entity"]
            }
        )["id"]
        
        data = {
            "permission_id": permission_id,
            "permission_name": request["permission"],
            "entity": request['entity'],
            "user_id": request["user_id"],
        }
        
        check_existed = self.user_permission_repository.select(data)

        if check_existed != []:
            return "This user has already had this permission", 400

        response = self.user_permission_repository.insert(data)
        return {"data": response}

    def get_cur_user_permission(self, req):
        user_id = req["user_id"]
        entity = req["entity"]
        response = None

        response = self.user_permission_repository.select_permission_entity(user_id, entity)
        return response

    def get_entity_properties(req):
        entity = req["entity"]
        
    def loaded_user(self, user_id):
        return self.user_repository.loaded_user(user_id)

    def get_player_by_id(self, id):
        return self.player_repository.select_by_id(id)
        
    def get_permission_by_id(self, id):
        return self.permission_repository.select_by_id(id)

    def get_user_by_id(self, id):
        return self.user_repository.select_by_id(id)

    def get_group_by_id(self, id):
        return self.group_repository.select_by_id(id)

    def get_football_club_by_id(self, id):
        return self.football_club_repository.select_by_id(id)

    def get_league_by_id(self, id):
        return self.league_repository.select_by_id(id)

    def delete_player(self, id):
        res = self.player_repository.drop_row(id)
        return res

    def delete_football_club(self, id):
        res = self.football_club_repository.drop_row(id)
        return res

    def delete_user(self, id):
        res = self.user_repository.drop_row(id)
        self.user_group_repository.drop_row(id)
        self.user_permission_repository.drop_row(id)
        return res

    def get_group_by_user_id(self, user_id):
        return self.user_group_repository.select_user_group(user_id=user_id)
