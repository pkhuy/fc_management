import re
from flask import json
from entities.player import Player
from entities.user import User
from database.db_config import DBConnectionHandler
from database.model import UserGroup as UserGroupModel
from database.model import Player as PlayerModel
from database.model import Group as GroupModel
from entities.user_group import UserGroup
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import text

class UserGroupRepository:
    @classmethod
    def insert(cls, user_id:int, group_id: int) -> UserGroupModel:
        with DBConnectionHandler() as db_connection:
            try:
                new_user_group = UserGroupModel(
                    user_id=user_id, group_id=group_id)
                db_connection.session.add(new_user_group)
                db_connection.session.commit()

                return UserGroup(
                    id=new_user_group.id, user_id=new_user_group.user_id, group_id=new_user_group.group_id
                )
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select_all(cls) -> List[UserGroup]:
        with DBConnectionHandler() as db_connection:
            try:
                datas = (
                    db_connection.session.query(PlayerModel).all()
                )
                json_datas = []
                for data in datas:
                    json_datas.append(
                        UserGroup(data.id, data.user_id, data.group_id).get_as_json())

                return json_datas

            except NoResultFound:
                return []
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select_user_group(cls, user_id: int) -> List[GroupModel]:
        
        with DBConnectionHandler() as db_connection:
            try:
                query_data = None
                res = []
                if user_id:
                    data = text("""SELECT groups.name
                                    FROM users, user_group, groups
                                    WHERE users.id = {} 
                                    AND users.id = user_group.user_id
                                    AND user_group.group_id = groups.id""".format(user_id))
                    query_data = db_connection.get_engine().execute(data)

                    groups = [row for row in query_data]

                    for group in groups:
                        res.append(group[0])
                return res

            except NoResultFound:
                return []
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

        return None


    @classmethod
    def update(cls, req) -> Player:

        with DBConnectionHandler() as db_connection:
            try:
                json_data = None
                id = int(req["id"])
                if id:
                    # Select player by id
                    with DBConnectionHandler() as db_connection:
                        for key in req.keys():
                            db_connection.session.query(
                                UserGroupModel).filter_by(id=id).\
                                update({str(key): (req[key])})
                            db_connection.session.commit()

                        data = db_connection.session.query(
                            UserGroupModel).filter_by(id=id).one()

                        json_data = UserGroup(
                            data.id, data.user_id, data.group_id).get_as_json()
                return json_data

            except NoResultFound:
                return []
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def drop_row(cls, user_id):

        with DBConnectionHandler() as db_connection:
            dropable = False
            try:
                if id:
                    data = db_connection.session.query(
                        UserGroupModel).filter_by(user_id=user_id).all()
                    for delete_data in data:
                        db_connection.session.delete(delete_data)
                        db_connection.session.commit()
            except NoResultFound:
                return dropable
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()
