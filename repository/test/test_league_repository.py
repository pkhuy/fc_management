from entities.player import Player
from entities.user import User
from database.db_config import DBConnectionHandler
from database.model import User as UserModel
from database.model import Player as PlayerModel
from database.model import League as LeagueModel
from entities.league import League
from typing import List
from sqlalchemy.orm.exc import NoResultFound


class LeagueRepository:
    @classmethod
    def insert(cls, req: dict) -> League:
        with DBConnectionHandler() as db_connection:
            try:
                new_league = LeagueModel(
                    name=req["name"], quantity=req["quantity"])
                db_connection.session.add(new_league)
                db_connection.session.commit()

                return Player(
                    id=new_league.id, name=new_league.name, quantity=new_league.quantity
                ).get_as_json()

            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def insert_one(cls, name, quantity) -> LeagueModel:
        # Creating a Return Tuple With Informations

        with DBConnectionHandler() as db_connection:
            try:
                new_league = LeagueModel(
                    name=name, quantity=quantity)
                db_connection.session.add(new_league)
                db_connection.session.commit()

                return League(
                    id=new_league.id, email=new_league.name, quantity=new_league.quantity
                )

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
                json_datas = []
                for data in datas:
                    json_datas.append(
                        League(data.id, data.name, data.quantity).get_as_json())

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
                    # Select player by id
                    with DBConnectionHandler() as db_connection:
                        data = db_connection.session.query(
                            LeagueModel).filter_by(id=id).one()
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
