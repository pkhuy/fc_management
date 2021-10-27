from database.db_config import DBConnectionHandler
from database.model import LeagueFC as LeagueFCTable
from entities.league_fc import LeagueFC
from typing import List
from sqlalchemy.orm.exc import NoResultFound


class LeagueFCRepository:
    @classmethod
    def insert(cls, data: dict) -> LeagueFC:
        # Creating a Return Tuple With Informations

        with DBConnectionHandler() as db_connection:
            try:
                new_league_com = LeagueFCTable(
                    league_id=data["league_id"], fc_id=data["fc_id"])
                db_connection.session.add(new_league_com)
                db_connection.session.commit()

                return LeagueFC(
                    new_league_com.id, new_league_com.league_id, new_league_com.fc_id
                ).get_as_json()

            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select(cls, data) -> LeagueFC:

        with DBConnectionHandler() as db_connection:
            try:
                league_com = db_connection.session.query(LeagueFCTable)\
                    .filter_by(league_id=data["league_id"], fc_id=data["fc_id"])\
                    .one()
                
                json_data = LeagueFC(league_com.id, league_com.id, league_com.fc_id).get_as_json()
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
    def select_all(cls) -> dict:
        with DBConnectionHandler() as db_connection:
            try:
                datas = (
                    db_connection.session.query(LeagueFCTable).all()
                )
                json_datas = {}
                for data in datas:
                    json_datas[str(data.id)] = LeagueFC(
                        data.id, data.league_id, data.fc_id).get_as_json()

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
    def select_by_id(cls, id: int) -> LeagueFC:

        with DBConnectionHandler() as db_connection:
            try:
                json_data = None

                data = db_connection.session.query(
                    LeagueFCTable).filter_by(id=id).one()
                json_data = LeagueFC(
                    data.id, data.league_id, data.fc_id).get_as_json()

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
    def update(cls, data) -> LeagueFC:
        with DBConnectionHandler() as db_connection:
            try:
                json_data = None
                id = int(data["id"])
                if id:
                    # Select player by id
                    with DBConnectionHandler() as db_connection:
                        league_com = db_connection.session.query(
                            LeagueFC).filter_by(id=id).one()
                        league_com.league_id = int(data["league_id"])
                        league_com.fc_id = int(data["fc_id"])
                        db_connection.session.commit()

                        data = db_connection.session.query(
                            LeagueFCTable).filter_by(id=id).one()
                        print(data)
                        json_data = LeagueFC(
                            data.id, data.league_id, data.fc_id).get_as_json()
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
    def drop_row(cls, league_id) -> bool:

        with DBConnectionHandler() as db_connection:
            dropable = False
            try:
                if id:
                    data = db_connection.session.query(
                        LeagueFCTable).filter_by(league_id=league_id).one()
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
