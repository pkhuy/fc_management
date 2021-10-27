from database.db_config import DBConnectionHandler
from database.model import League as LeagueModel
from entities.league import League
from typing import List
from sqlalchemy.orm.exc import NoResultFound


class LeagueRepository:
    @classmethod
    def insert(cls, data: dict) -> League:
        # Creating a Return Tuple With Informations

        with DBConnectionHandler() as db_connection:
            try:
                new_league = LeagueModel(
                    name=data["name"], quantity=data["quantity"])
                db_connection.session.add(new_league)
                db_connection.session.commit()

                return League(
                    id=new_league.id, name=new_league.name, quantity=new_league.quantity
                ).get_as_json()

            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

        return None

    @classmethod
    def select_all(cls) -> List[League]:
        with DBConnectionHandler() as db_connection:
            try:
                datas = (
                    db_connection.session.query(LeagueModel).all()
                )
                json_datas = {}
                for data in datas:
                    json_datas[str(data.name)]=League(data.id, data.name, data.quantity).get_as_json()

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
    def select_by_id(cls, id: int) -> League:

        with DBConnectionHandler() as db_connection:
            try:
                json_data = None

                if id:
                    with DBConnectionHandler() as db_connection:
                        data = db_connection.session.query(
                            LeagueModel).filter_by(id=id).one()
                        json_data = League(
                            data.id, data.name, data.quantity).get_as_json()

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
    def update(cls, data) -> League:
        with DBConnectionHandler() as db_connection:
            try:
                json_data = None
                id = int(data["id"])
                if id:
                    with DBConnectionHandler() as db_connection:
                        league = db_connection.session.query(
                            LeagueModel).filter_by(id=id).one()
                        league.name = str(data["name"])
                        league.quantity = str(data["quantity"])
                        db_connection.session.commit()

                        data = db_connection.session.query(
                            LeagueModel).filter_by(id=id).one()
                        print(data)
                        json_data = League(
                            data.id, data.name, data.quantity).get_as_json()
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
    def drop_row(cls, id) -> bool:

        with DBConnectionHandler() as db_connection:
            dropable = False
            try:
                if id:
                    data = db_connection.session.query(
                        LeagueModel).filter_by(id=id).one()
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
