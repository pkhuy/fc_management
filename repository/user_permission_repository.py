import re
from flask import json
from entities.player import Player
from entities.user import User
from database.db_config import DBConnectionHandler
from database.model import UserPermission as UserPermissionModel
from database.model import Player as PlayerModel
from database.model import Group as GroupModel
from database.model import User as UserModel
from database.model import Permission as PermissionModel
from entities.user_permission import UserPermission
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import text


class UserPermissionRepository:
    @classmethod
    def insert(cls, data: dict) -> UserPermissionModel:
        with DBConnectionHandler() as db_connection:
            try:
                new_user_permission = UserPermissionModel(
                    user_id=data["user_id"], permission_id=data["permission_id"])
                db_connection.session.add(new_user_permission)
                db_connection.session.commit()

                return UserPermission(
                    id=new_user_permission.id,
                    user_id=new_user_permission.user_id,
                    permission_id=new_user_permission.permission_id
                ).get_as_json()
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select(cls, sv_data) -> List[UserPermission]:
        with DBConnectionHandler() as db_connection:
            try:
                rp_data = (
                    db_connection.session.query(UserPermissionModel).filter_by(
                        user_id=sv_data["user_id"], permission_id=sv_data["permission_id"]
                    ).one()
                )
                json_datas = UserPermission(rp_data.id, rp_data.user_id, rp_data.permission_id).get_as_json()

                return json_datas

            except NoResultFound:
                return None
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
                    db_connection.session.query(UserPermissionModel).all()
                )
                json_datas = []
                for data in datas:
                    json_datas.append(
                        UserPermission(data.id, data.user_id, data.permission_id).get_as_json())

                return json_datas

            except NoResultFound:
                return None
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select_by_id(cls, user_id: int, permission_id) :
        db_conn = DBConnectionHandler()
        data = db_conn.execute(text("""SELECT * FROM user_permission WHERE user_id={} AND permission_id={}"""
                        .format(user_id, permission_id))).fetchone()
        json_data=UserPermission(data.id, data.user_id, data.permission_id).get_as_json()
        return json_data

    @classmethod
    def select_by_user_id(cls, user_id: int) :
        db_conn = DBConnectionHandler()
        datas = db_conn.execute(text("""SELECT * FROM user_permission WHERE user_id={}"""
                        .format(user_id))).fetchall()
        json_data = {}
        for data in datas:
            json_data["id "+ str(data.id)]=UserPermission(data.id, data.user_id, data.permission_id).get_as_json()
        return json_data

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
            try:
                if id:
                    data = db_connection.session.query(
                        UserPermissionModel).filter_by(user_id=user_id).all()
                    for delete_data in data:
                        db_connection.session.delete(delete_data)
                        db_connection.session.commit()
            except NoResultFound:
                return None
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def drop_row_by_id(cls, id):

        with DBConnectionHandler() as db_connection:
            try:
                if id:
                    rp_data = db_connection.session.query(
                        UserPermissionModel).filter_by(id=id).one()
                    db_connection.session.delete(rp_data)
                    db_connection.session.commit()
            except NoResultFound:
                return None
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    #get_permission_that_user_have_to_manage_the_entity
    @classmethod
    def select_permission_entity(cls, user_id: int, entity: str) -> List[PermissionModel]:
        with DBConnectionHandler() as db_connection:
            try:
                query_data = None
                res = []

                if user_id:
                    # Select user by id
                    with DBConnectionHandler() as db_connection:
                        data = text("""SELECT permissions.name, permissions.entity
                                        FROM users, user_group, group_permission, permissions 
                                        WHERE users.id = {} 
                                        AND users.id = user_group.user_id
                                        AND user_group.group_id = group_permission.group_id
                                        AND group_permission.permission_id = permissions.id""".format(user_id))

                        query_data = db_connection.get_engine().execute(data)

                        permissions = [row for row in query_data]

                        for permission in permissions:
                            
                            if permission[1] == entity:
                                res.append(permission[0])
                                print(permission[0])

                        data = text("""SELECT permissions.name, permissions.entity
                                        FROM users, user_permission, permissions 
                                        WHERE users.id = {} 
                                        AND users.id = user_permission.user_id
                                        AND user_permission.user_id = permissions.id""".format(user_id))

                        query_data = db_connection.get_engine().execute(data)

                        permissions = [row for row in query_data]

                        for permission in permissions:
                            #print(permission)
                            if permission[1] == entity and permission[0] not in res:
                                res.append(permission[0])
                print(res)
                return res

            except NoResultFound:
                return []
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()
