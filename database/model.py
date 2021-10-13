from datetime import date, datetime
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from sqlalchemy.sql.schema import ForeignKey, Table
from database.db_base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from flask_login import LoginManager

class User(Base, UserMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, nullable=False)
    password = Column(String)
    def __repr__(self) -> str:
        return f"User('{self.name}', '{self.email}' )"

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    #content = Column(String)
    entity = Column(String)

class UserGroup(Base):
    __tablename__ = "user_group"

    user_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, primary_key=True)


class UserPermission(Base):
    __tablename__ = "user_permission"

    user_id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, primary_key=True)


class GroupPermission(Base):
    __tablename__ = "group_permission"

    group_id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, primary_key=True)


class League(Base):
    __tablename__ = "league"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)


class FootballClub(Base):
    __tablename__ = "football_club"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    position = Column(String)
    fc_id = Column(Integer)


class LeagueFC(Base):
    __tablename__ = "league_football_club"

    league_id = Column(Integer, primary_key=True)
    football_club_id = Column(Integer, primary_key=True)

'''    
UserGroup = Table("user_group", Base.metadata,
                  Column('id', Integer, primary_key=True),
                  Column('user_id', Integer, ForeignKey('users.id')),
                  Column('group_id', Integer, ForeignKey('groups.id'))
)
    
UserPermission = Table("user_permission", Base.metadata,
                  Column('id', Integer, primary_key=True),
                  Column('user_id', Integer, ForeignKey('users.id')),
                  Column('permission_id', Integer, ForeignKey('permisisons.id'))
)

GroupPermission = Table("group_permission", Base.metadata,
                  Column('id', Integer, primary_key=True),
                  Column('group_id', Integer, ForeignKey('groups.id')),
                  Column('permission_id', Integer, ForeignKey('permisisons.id'))
)'''
