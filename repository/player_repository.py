import re
from flask import json
from entities.player import Player
from entities.user import User
from database.db_config import DBConnectionHandler
from database.model import User as UserModel
from database.model import Player as PlayerModel
from entities.player import Player
from typing import List
from sqlalchemy.orm.exc import NoResultFound


class PlayerRepository:
    @classmethod
    def insert(cls, req: dict) -> Player:
        with DBConnectionHandler() as db_connection:
            try:
                new_player = PlayerModel(
                    name=req["name"], position=req["position"], fc_id=req["fc_id"])
                db_connection.session.add(new_player)
                db_connection.session.commit()

                return Player(
                    id=new_player.id, name=new_player.name, position=new_player.position, fc_id=new_player.fc_id
                ).get_as_json()

            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select_all(cls) -> List[Player]:
        with DBConnectionHandler() as db_connection:
            try:
                datas = (
                    db_connection.session.query(PlayerModel).all()
                )
                json_datas = {}
                for data in datas:
                    json_datas[str(data.name)]=Player(data.id, data.name, data.position, data.fc_id).get_as_json()

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
    def select_by_id(cls, id: int) -> Player:

        with DBConnectionHandler() as db_connection:
            try:
                json_data = None

                if id:
                    # Select player by id
                    with DBConnectionHandler() as db_connection:
                        data = db_connection.session.query(
                            PlayerModel).filter_by(id=id).one()
                        json_data = Player(
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
    def update(cls, data) -> Player:

        with DBConnectionHandler() as db_connection:
            try:
                json_data = None
                id = int(data["id"])
                if id:
                    # Select player by id
                    with DBConnectionHandler() as db_connection:
                        player = db_connection.session.query(
                            PlayerModel).filter_by(id=id).one()
                        player.name=str(data["name"]) 
                        player.position=str(data["position"])
                        player.fc_id=int(data["fc_id"])
                        db_connection.session.commit()

                        data = db_connection.session.query(
                            PlayerModel).filter_by(id=id).one()
                        print(data)
                        json_data = Player(
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
                        PlayerModel).filter_by(id=id).one()
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
