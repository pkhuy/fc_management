from abc import ABC, ABCMeta
from database.db_config import DBConnectionHandler

class BaseRepository(ABC):
    @classmethod
    def insert(cls, data):
        pass

    @classmethod
    def select(cls):
        pass
    
    @classmethod
    def select_by(cls, data):
        pass

    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, data):
        pass