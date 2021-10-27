import re
from flask import json
from entities.player import Player
from entities.user import User
from database.db_config import DBConnectionHandler
from database.model import UserPermission as UserPermissionModel
from database.model import Player as PlayerModel
from database.model import Group as GroupModel
from entities.user_permission import UserPermission
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import text


class UserPermissionRepository:
    @classmethod
    def insert(cls, user_id: int, permission_id: int) -> UserPermissionModel:
        with DBConnectionHandler() as db_connection:
            try:
                new_user_permission = UserPermissionModel(
                    user_id=user_id, permission_id=permission_id)
                db_connection.session.add(new_user_permission)
                db_connection.session.commit()

                return UserPermission(
                    id=new_user_permission.id, 
                    user_id=new_user_permission.user_id, 
                    permission_id=new_user_permission.permission_id
                )
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select_all(cls) -> List[UserPermission]:
        with DBConnectionHandler() as db_connection:
            try:
                datas = (
                    db_connection.session.query(PlayerModel).all()
                )
                json_datas = []
                for data in datas:
                    json_datas.append(
                        UserPermission(data.id, data.user_id, data.group_id).get_as_json())

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
        """
        Select data in user entity by id and/or name
        :param  - id: Id of the registry
                - name: User name in database
        :return - List with UsersModel selected
        """
        with DBConnectionHandler() as db_connection:
            try:
                query_data = None

                if user_id:
                    # Select user by id
                    with DBConnectionHandler() as db_connection:
                        data = text("""SELECT DISTINCT(groups.name)
                                        FROM users, user_group, groups
                                        WHERE users.id = {} 
                                        AND users.id = user_group.user_id
                                        AND user_group.group_id = groups.id""".format(user_id))
                        query_data = [data]

                return query_data

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
                                UserPermissionModel).filter_by(id=id).\
                                update({str(key): (req[key])})
                            db_connection.session.commit()

                        data = db_connection.session.query(
                            UserPermissionModel).filter_by(id=id).one()

                        json_data = UserPermission(
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
                        UserPermissionModel).filter_by(user_id=user_id).all()
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
