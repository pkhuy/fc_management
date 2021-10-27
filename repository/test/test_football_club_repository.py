from entities.player import Player
from entities.user import User
from database.db_config import DBConnectionHandler
from database.model import FootballClub as FootballClubModel
from entities.football_club import FootballClub
from database.model import Player as PlayerModel
from database.model import League as LeagueModel
from entities.league import League
from typing import List
from sqlalchemy.orm.exc import NoResultFound


class FootballClubRepository:
    @classmethod
    def insert(cls, req: dict) -> FootballClub:
        with DBConnectionHandler() as db_connection:
            try:
                new_football_club = FootballClubModel(
                    name=req["name"], quantity=req["name"])
                db_connection.session.add(new_football_club)
                db_connection.session.commit()

                return FootballClub(
                    id=new_football_club.id, name=new_football_club.name, quantity=new_football_club.quantity
                ).get_as_json()

            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select_all(cls) -> List[FootballClub]:
        with DBConnectionHandler() as db_connection:
            try:
                datas = (
                    db_connection.session.query(FootballClubModel).all()
                )
                json_datas = []
                for data in datas:
                    json_datas.append(
                        FootballClub(data.id, data.name, data.quantity).get_as_json())

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
    def select_by_id(cls, id: int) -> FootballClub:

        with DBConnectionHandler() as db_connection:
            try:
                json_data = None

                if id:
                    # Select player by id
                    with DBConnectionHandler() as db_connection:
                        data = db_connection.session.query(
                            FootballClubModel).filter_by(id=id).one()
                        json_data = FootballClub(
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
    def update(cls, req) -> FootballClub:
        with DBConnectionHandler() as db_connection:
            try:
                json_data = None
                id = int(req["id"])
                if id:
                    # Select player by id
                    with DBConnectionHandler() as db_connection:
                        for key in req.keys():
                            db_connection.session.query(
                                FootballClubModel).filter_by(id=id).\
                                update({str(key): (req[key])})
                            db_connection.session.commit()

                        data = db_connection.session.query(
                            FootballClubModel).filter_by(id=id).one()
                        print(data)
                        json_data = FootballClub(
                            data.id, data.name, data.position, data.fc_id).get_as_json()
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
                        FootballClubModel).filter_by(id=id).one()
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
