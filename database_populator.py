from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from database_setup import Base, User, Game, Complete

engine = create_engine('sqlite:///ghosts.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

users = session.query(User)
usernames = []
for user in users:
    usernames.append(user.name)

names=['admin', 'josh', 'adam', 'paul', 'stephen', 'james', 'jonathan']
passwords=['admin', 'josh', 'adam', 'paul', 'stephen', 'james', 'jonathan']

for x in range(0,len(names)):
    if names[x] in usernames:
        print names[x] + " exists already"
    else:
        newUser = User(name=names[x], password=passwords[x], email="joshbriand@gmail.com", notifications="no")
        session.add(newUser)
        session.commit()
        print names[x] + " added"

'''
player1 = [2, 3, 4, 5, 6]
player2 = [3, 2, 2, 2, 2]
date = datetime.now()
positions = ''
previousPlayer = [2, 0, 1, 2, 1]
previousGhost = 'none'

for x in range(0, len(player1)):
    newGame = Game(
        player1id = player1[x],
        player2id = player2[x],
        date = date,
        b11 = 'p2b1',
        b21 = '',
        b31 = 'p2b3',
        b41 = 'p2b4',
        b51 = 'p2y1',
        b61 = 'p2y2',
        b12 = '',
        b22 = '',
        b32 = 'p2y3',
        b42 = 'p2y4',
        b52 = 'p1y4',
        b62 = '',
        b13 = '',
        b23 = '',
        b33 = '',
        b43 = '',
        b53 = '',
        b63 = '',
        b14 = '',
        b24 = '',
        b34 = '',
        b44 = '',
        b54 = '',
        b64 = '',
        b15 = '',
        b25 = '',
        b35 = '',
        b45 = '',
        b55 = '',
        b65 = 'p1y3',
        b16 = 'p1y2',
        b26 = 'p1y1',
        b36 = 'p1b4',
        b46 = 'p1b3',
        b56 = 'p1b2',
        b66 = '',
        previousPlayer = previousPlayer[x],
        previousGhost = previousGhost)
    session.add(newGame)
    session.commit()
print "games in progress added"

player1 = [2,3,4,3,5]
player2 = [3,2,2,2,2]
winner = [2,3,4,2,5]
completed = datetime.now()
won = ['blue','exit','yellow','blue','exit']

for x in range(0, len(player1)):
    completeGame = Complete(
        gameid=777,
        player1id=player1[x],
        player2id=player2[x],
        winnerid=winner[x],
        completed=completed,
        won=won[x]
    )
    session.add(completeGame)
    session.commit()
print "completed games added"
'''
