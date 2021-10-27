from sqlalchemy.sql.expression import text
from database.db_config import DBConnectionHandler
from database.model import Permission as PermissionModel
from database.model import User as UserModel
from database.model import Group as GroupModel
from database.model import UserPermission
from database.model import GroupPermission
from entities.permission import Permission
from typing import List
from sqlalchemy.orm.exc import NoResultFound


class PermissionRepository:
    @classmethod
    def insert(cls, req: dict) -> Permission:
        with DBConnectionHandler() as db_connection:
            try:
                new_permission = PermissionModel(
                    name=req["name"], entity=req["entity"])
                db_connection.session.add(new_permission)
                db_connection.session.commit()

                return Permission(
                    name=new_permission.name, entity=new_permission.entity
                ).get_as_json()

            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select(cls, data) -> List[Permission]:
        with DBConnectionHandler() as db_connection:
            try:
                data_res = (
                    db_connection.session.query(PermissionModel).filter_by(
                        name=data["permission_name"], entity=data["entity"]
                    ).one()
                )
                return Permission(data_res.id, data_res.name, data_res.entity).get_as_json()

            except NoResultFound:
                return []
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select_all(cls) -> dict:
        with DBConnectionHandler() as db_connection:
            try:
                datas = (
                    db_connection.session.query(PermissionModel).all()
                )
                json_datas = {}
                for data in datas:
                    json_datas[str(data.name+'-'+data.entity)]=Permission(data.id, data.name, data.entity).get_as_json()

                return json_datas

            except NoResultFound:
                return {}
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()
    # create

    @classmethod
    def insert_user_permission(cls, user: UserModel, permission: PermissionModel) -> PermissionModel:
        # Creating a Return Tuple With Informations

        with DBConnectionHandler() as db_connection:
            try:
                new_up = UserPermission(
                    user_id=user.id, permission_id=permission.id)
                db_connection.session.add(new_up)
                db_connection.session.commit()

                return UserPermission(
                    id=new_up.id, user_id=new_up.user_id, permission_id=new_up.permission_id
                )

            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    #create
    @classmethod
    def insert_group_permission(cls, group: GroupModel, permission: PermissionModel) -> PermissionModel:
        # Creating a Return Tuple With Informations

        with DBConnectionHandler() as db_connection:
            try:
                new_gp = GroupPermission(
                    group_id=group.id, permission_id=permission.id)
                db_connection.session.add(new_gp)
                db_connection.session.commit()

                return GroupPermission(
                    id=new_gp.id, group_id=new_gp.group_id, permission_id=new_gp.permission_id
                )

            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def get_id(cls, name: str, entity: str) -> int:
        with DBConnectionHandler() as db_connection:
            try:
                data = None
                if name and entity:
                    # Select user by id
                    with DBConnectionHandler() as db_connection:
                        data = db_connection.query(PermissionModel
                                                   ).filter(name=name, entity=entity)

                return data.id

            except NoResultFound:
                return []
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

        return None
    
    #moved to u_p_repo
    @classmethod
    def select_permission_entity(cls, user: UserModel, entity: str) -> List[PermissionModel]:
        with DBConnectionHandler() as db_connection:
            try:
                query_data = None
                res = []

                if user:
                    # Select user by id
                    with DBConnectionHandler() as db_connection:
                        data = text("""SELECT permissions.name, permissions.entity
                                        FROM users, user_group, group_permission, permissions 
                                        WHERE users.id = {} 
                                        AND users.id = user_group.user_id
                                        AND user_group.group_id = group_permission.group_id
                                        AND group_permission.permission_id = permissions.id""".format(user.id))

                        query_data = db_connection.get_engine().execute(data)

                        permissions = [row for row in query_data]

                        for permission in permissions:
                            if permission[1] == entity:
                                res.append(permission[0])

                        data = text("""SELECT permissions.name, permissions.entity
                                        FROM users, user_permission, permissions 
                                        WHERE users.id = {} 
                                        AND users.id = user_permission.user_id
                                        AND user_permission.user_id = permissions.id""".format(user.id))

                        query_data = db_connection.get_engine().execute(data)

                        permissions = [row for row in query_data]

                        for permission in permissions:
                            if permission[1] == entity and permission[0] not in res:
                                res.append(permission[0])
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
    def select_by_id(cls, id: int) -> Permission:

        with DBConnectionHandler() as db_connection:
            try:
                json_data = None

                if id:
                    # Select player by id
                    with DBConnectionHandler() as db_connection:
                        data = db_connection.session.query(
                            PermissionModel).filter_by(id=id).one()
                        json_data = Permission(
                            data.id, data.name, data.entity).get_as_json()

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
    def select_by_name(cls, name) -> Permission:

        with DBConnectionHandler() as db_connection:
            try:
                json_data = None

                if id:
                    # Select player by id
                    with DBConnectionHandler() as db_connection:
                        data = db_connection.session.query(
                            PermissionModel).filter_by(name=name).one()
                        json_data = Permission(
                            data.id, data.name, data.entity).get_as_json()

                return json_data

            except NoResultFound:
                return []
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()
