import bcrypt
from entities.user import User
from database.db_config import DBConnectionHandler
from database.model import User as UserModel
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import text

class UserRepository:
    @classmethod
    def insert_user(cls, data) -> UserModel:
        with DBConnectionHandler() as db_connection:
            try:
                hash_pass = bcrypt.hashpw(
                    data["password"].encode('utf-8'), bcrypt.gensalt())
                new_user = UserModel(name=data["name"], email=data["email"], password=hash_pass)
                db_connection.session.add(new_user)
                db_connection.session.commit()
                return User(
                    id=new_user.id, name=new_user.name, email=new_user.email
                )
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select_all(cls) -> List[User]:
        db_conn = DBConnectionHandler()
        datas = db_conn.execute(text("""SELECT * FROM users"""))
        print(datas)
        json_datas = {}
        for data in datas:
            json_datas[str(data.name)] = User(
                data.id, data.name, data.email).get_as_json()
        return json_datas


    @classmethod
    def select(cls, data) -> List[UserModel]:
        
        with DBConnectionHandler() as db_connection:
            try:
                user = (
                    db_connection.session.query(UserModel)
                    .filter_by(email=str(data["email"]))
                    .one()
                )
                if bcrypt.checkpw(str(data["password"]).encode('utf-8'), user.password):
                    return user
                else:
                    return None

            except NoResultFound:
                return []
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select_by_id(cls, id: int) -> User:

        with DBConnectionHandler() as db_connection:
            try:
                json_data = None

                if id:
                    # Select player by id
                    with DBConnectionHandler() as db_connection:
                        data = db_connection.session.query(
                            UserModel).filter_by(id=id).one()
                        json_data = User(
                            data.id, data.name, data.email, data.password).get_as_json()

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
    def select_by_email(cls, email: str) -> User:

        with DBConnectionHandler() as db_connection:
            try:
                json_data = None

                if email:
                    data = db_connection.session.query(
                        UserModel).filter_by(email=email).one()
                    json_data = User(
                        data.id, data.name).get_as_json()
                    print(json_data)
                return json_data

            except NoResultFound:
                return None
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def loaded_user(cls, id: int) -> UserModel:
        with DBConnectionHandler() as db_connection:
            try:
                data = None

                if id:
                    # Select user by id
                    with DBConnectionHandler() as db_connection:
                        data = (
                            db_connection.session.query(UserModel)
                            .filter_by(id=id)
                            .one()
                        )

                return data

            except NoResultFound:
                return data
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def update(cls, data) -> User:

        with DBConnectionHandler() as db_connection:
            try:
                json_data = None
                id = int(data["id"])
                user=db_connection.session.query(
                    UserModel).filter_by(id=id).one()
                user.name = data["name"]
                user.email = data["email"]
                user.password = bcrypt.hashpw(
                    data["password"].encode('utf-8'), bcrypt.gensalt())
                db_connection.session.commit()

                data = db_connection.session.query(
                    UserModel).filter_by(id=id).one()
                json_data = User(
                    data.id, data.name, data.email, data.password).get_as_json()
                return json_data

            except NoResultFound:
                return []
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    #Not done yet
    @classmethod
    def get_permission(cls, entity: str) -> UserModel:
        with DBConnectionHandler() as db_connection:
            try:
                data = None

                if id:
                    # Select user by id
                    with DBConnectionHandler() as db_connection:
                        data = (
                            db_connection.session.query(UserModel)
                            .filter_by(id=id)
                            .one()
                        )

                return data

            except NoResultFound:
                return data
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def drop_row(cls, id) -> bool:

        with DBConnectionHandler() as db_connection:
            dropable = False
            try:
                if id:
                    data = db_connection.session.query(
                        UserModel).filter_by(id=id).one()
                    db_connection.session.delete(data)
                    db_connection.session.commit()
            except NoResultFound:
                return dropable
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()
