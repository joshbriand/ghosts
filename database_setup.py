from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    notifications = Column(String(2), nullable=False)

class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    player1id = Column(Integer, ForeignKey('user.id'))
    player2id = Column(Integer, ForeignKey('user.id'))
    date = Column(DateTime)
    b11 = Column(String(4))
    b21 = Column(String(4))
    b31 = Column(String(4))
    b41 = Column(String(4))
    b51 = Column(String(4))
    b61 = Column(String(4))
    b12 = Column(String(4))
    b22 = Column(String(4))
    b32 = Column(String(4))
    b42 = Column(String(4))
    b52 = Column(String(4))
    b62 = Column(String(4))
    b13 = Column(String(4))
    b23 = Column(String(4))
    b33 = Column(String(4))
    b43 = Column(String(4))
    b53 = Column(String(4))
    b63 = Column(String(4))
    b14 = Column(String(4))
    b24 = Column(String(4))
    b34 = Column(String(4))
    b44 = Column(String(4))
    b54 = Column(String(4))
    b64 = Column(String(4))
    b15 = Column(String(4))
    b25 = Column(String(4))
    b35 = Column(String(4))
    b45 = Column(String(4))
    b55 = Column(String(4))
    b65 = Column(String(4))
    b16 = Column(String(4))
    b26 = Column(String(4))
    b36 = Column(String(4))
    b46 = Column(String(4))
    b56 = Column(String(4))
    b66 = Column(String(4))
    previousPlayer = Column(Integer, ForeignKey('user.id'))
    previousGhost = Column(String(4), nullable=False)

class Complete(Base):
    __tablename__ = 'complete'

    id = Column(Integer, primary_key=True)
    gameid = Column(Integer,nullable=False)
    player1id = Column(Integer, ForeignKey('user.id'))
    player2id = Column(Integer, ForeignKey('user.id'))
    winnerid = Column(Integer, ForeignKey('user.id'))
    completed = Column(DateTime)
    won = Column(String(6))


engine = create_engine('sqlite:///ghosts.db')


Base.metadata.create_all(engine)
