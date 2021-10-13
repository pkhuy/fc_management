from sqlalchemy.sql.expression import text
from database.db_config import DBConnectionHandler
from database.model import Permission as PermissionModel
from database.model import User as UserModel
from database.model import Group as GroupModel
from database.model import UserPermission
from database.model import UserGroup
from database.model import GroupPermission
from typing import List
from sqlalchemy.orm.exc import NoResultFound


class PermissionRepository:
    #create
    @classmethod
    def insert_user_permission(cls, user: UserModel, permission: PermissionModel) -> PermissionModel:
        # Creating a Return Tuple With Informations

        with DBConnectionHandler() as db_connection:
            try:
                new_up = UserPermission(user_id=user.id, permission_id=permission.id)
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
                new_gp = GroupPermission(group_id=group.id, permission_id=permission.id)
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

    #read but not use
    @classmethod
    def select_user_permission(cls, user: UserModel, permission: PermissionModel) -> PermissionModel:
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

    @classmethod
    def get_id(cls, name: str, entity: str) -> int:
        with DBConnectionHandler() as db_connection:
            try:
                data=None
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

    @classmethod
    def select_permission(cls, user: UserModel, entity: str) -> List[PermissionModel]:
        with DBConnectionHandler() as db_connection:
            try:
                query_data = None

                if user:
                    # Select user by id
                    with DBConnectionHandler() as db_connection:
                        data = text("""SELECT DISTINCT(permissions.name)
                                        FROM users, user_group, group_permission, permissions 
                                        WHERE users.id = {} 
                                        AND users.id = user_group.user_id
                                        AND user_group.group_id = group_permission.group_id
                                        AND group_permission.permission_id = permissions.id""".format(user.id))

                        query_data = db_connection.get_engine().execute(data)

                        permissions = [row[0] for row in query_data]
                        print(permissions, type(entity))
                        res = []
                        for permission in permissions:
                            if permission.entity is entity:
                                res.append(permission)

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
