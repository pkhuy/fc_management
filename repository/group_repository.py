from database.model import User as UserModel
from database.db_config import DBConnectionHandler
from database.model import Group as GroupModel
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import text
from entities.group import Group
class GroupRepository:
    '''def execute(self):
        if self.repository.find_by(self.email):
            raise 'Email already exists'
        user = self.factory_group()
        return self.repository.create(user)

    def factory_group(self) -> Group:
        instance = Group(self.groupname)
        return instance'''

    @classmethod
    def insert_group(cls, groupname: str) -> GroupModel:
        """
        Insert data in user entity
        :param  - name: person name
                - password: user password
        :return - tuple with new user inserted informations
        """

        # Creating a Return Tuple With Informations

        with DBConnectionHandler() as db_connection:
            try:
                new_group = GroupModel(groupname=groupname)
                db_connection.session.add(new_group)
                db_connection.session.commit()

                return Group(
                    id=new_group.id, groupname=new_group.groupname
                )

            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

        return None

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
