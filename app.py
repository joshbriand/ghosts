from flask import (
    Flask, render_template, request, redirect, jsonify, url_for, flash)
from flask import session as login_session
from flask import make_response, escape
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import (
    Base, User, Game, Complete)
import random
import string
from datetime import datetime
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import simplejson
import json
import ast
import requests
import re, hmac

app = Flask(__name__)

engine = create_engine('sqlite:///ghosts.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# code for Regular Expression validation
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")

#start of code for hashing
secret = "guest"

def validate(input, validation):
    return validation.match(input)

def hash_str(s):
    return hmac.new(secret, s).hexdigest()

def make_secure_val(password):
    return "%s" % (hash_str(password))

def check_secure_val(password):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val

def make_temp_password(password):
    return make_secure_val(password)

#end of code for hashing

#does user exist?
def userExists(name):
    q = session.query(User).filter_by(name=name)
    return session.query(q.exists()).scalar()

#does game exist?
def gameExists(name):
    q = session.query(Game).filter_by(id=id)
    return session.query(q.exists()).scalar()

def generateState():
    '''Create anti-forgery state token'''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return state


@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if request.form['login'] == "Log In":
            login_username = request.form['username']
            login_password = request.form['password']
            if login_username:
                if login_password:
                    users = session.query(User)
                    user = users.filter_by(name=login_username).one()
                    login_hashed_password = make_secure_val(login_password)
                    if userExists(login_username):
                        if user.name == login_password:
                            login_session['username'] = login_username
                            return redirect(url_for('changepassword'))
                        elif user.password == login_hashed_password:
                            login_session['username'] = login_username
                            return redirect(url_for('menu'))
                        else:
                            flash('Incorrect Password')
                            return render_template('login.html')
                    else:
                        flash('Username Not Found')
                        return render_template('login.html')
                else:
                    flash('No Password Entered')
                    return render_template('login.html')
            elif login_password:
                flash('No Username Entered')
                return render_template('login.html')
        elif request.form['login'] == "Create User":
            new_username = request.form['newUsername']
            new_password = request.form['newPassword']
            confirm_password = request.form['confirmPassword']
            new_email = request.form['newEmail']
            new_hashed_password = make_secure_val(new_password)
            if new_username:
                if userExists(new_username):
                    flash('Username Already Exists')
                    return render_template('login.html')
                elif validate(new_username, USER_RE) is None:
                    flash('That is Not a Valid Username')
                    return render_template('login.html')
                else:
                    if new_password == confirm_password:
                        if validate(new_password, PASSWORD_RE) is None:
                            flash('That is Not a Valid Password')
                            return render_template('login.html')
                        elif new_email:
                            #TODO
                            #RE email
                            newUser = User(name=new_username,
                                        password=new_hashed_password,
                                        email=new_email,
                                        notifications="n")
                            session.add(newUser)
                            session.commit()
                            login_session['username'] = new_username
                            return redirect(url_for('menu'))
                        else:
                            newUser = User(name=new_username,
                                        password=new_hashed_password,
                                        email="none",
                                        notifications="n")
                            session.add(newUser)
                            session.commit()
                            login_session['username'] = new_username
                            return redirect(url_for('menu'))
                    else:
                        flash('Passwords Do Not Match')
                        return render_template('login.html')

            else:
                flash('No Username Entered')
                return render_template('login.html')

@app.route('/logout/')
def logout():
    login_session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/changepassword/', methods=['GET', 'POST'])
def changepassword():
    if 'username' in login_session:
        users = session.query(User)
        users = users.order_by(User.name.asc())
        user = users.filter_by(name=login_session['username']).one()
        if request.method == 'GET':
            flash('Please Change Your Password')
            return render_template('changepassword.html',
                                    playerUsername=login_session['username'],
                                    userid=user.id)
        elif request.method == 'POST':
            if "changePassword" in request.form:
                print "database " + user.password
                current_password = request.form['currentPassword']
                print "current " + current_password
                new_password = request.form['newPassword']
                print "new " + new_password
                confirm_password = request.form['confirmPassword']
                current_hashed_password = make_secure_val(current_password)
                new_hashed_password = make_secure_val(new_password)
                print "new hashed " + new_hashed_password
                if current_hashed_password == user.password or current_password == user.password:
                    if new_password != current_password:
                        if new_password == confirm_password:
                            user.password = new_hashed_password
                            session.add(user)
                            session.commit()
                            flash('Password Successfully Changed')
                            return redirect(url_for('menu'))
                        else:
                            flash('Passwords Do Not Match')
                            return redirect(url_for('changepassword'))
                    else:
                        flash('New Password Must Be Different Than Current Password')
                        return redirect(url_for('changepassword'))
                else:
                    flash('Incorrect Current Password')
                    return redirect(url_for('changepassword'))
    else:
        flash('Please log in')
        return render_template('login.html')



@app.route('/menu/', methods=['GET', 'POST'])
def menu():
    if 'username' in login_session:
        users = session.query(User)
        users = users.order_by(User.name.asc())
        user = users.filter_by(name=login_session['username']).one()
        userNotification = user.notifications
        userGames = session.query(Game).filter((Game.player1id==user.id) | (Game.player2id==user.id))
        userGames = userGames.order_by(Game.id.asc())
        for game in userGames:
            print game.id
        userCompleted = session.query(Complete).filter((Complete.player1id==user.id) | (Complete.player2id==user.id)).all()
        userWins = session.query(Complete).filter(Complete.winnerid==user.id).all()
        blueWins = 0
        yellowWins = 0
        exitWins = 0
        for win in userWins:
            if win.won == 'blue':
                blueWins += 1
            elif win.won == 'yellow':
                yellowWins += 1
            elif win.won == 'exit':
                exitWins += 1
        if request.method == 'GET':
            return render_template('menu.html',
                                    playerUsername=login_session['username'],
                                    userid=user.id,
                                    users=users,
                                    userNotification=userNotification,
                                    userGames=userGames,
                                    userCompleted=userCompleted,
                                    userWins=userWins,
                                    blueWins=blueWins,
                                    yellowWins=yellowWins,
                                    exitWins=exitWins)
        elif request.method == 'POST':
            if "notifications" in request.form:
                notifications = request.form['notifications']
                print "-->" + notifications
                if notifications == 'on':
                    user.notifications = 'on'
                else:
                    user.notifications = 'no'
                session.add(user)
                session.commit()
                flash('Email Notifications Updated')
                return redirect(url_for('menu'))
            elif "changePassword" in request.form:
                current_password = request.form['currentPassword']
                new_password = request.form['newPassword']
                confirm_password = request.form['confirmPassword']
                current_hashed_password = make_secure_val(current_password)
                new_hashed_password = make_secure_val(new_password)
                if current_hashed_password == user.password:
                    if new_password != current_password:
                        if new_password == confirm_password:
                            user.password = new_hashed_password
                            session.add(user)
                            session.commit()
                            flash('Password Successfully Changed')
                            return redirect(url_for('menu'))
                        else:
                            flash('Passwords Do Not Match')
                            return redirect(url_for('menu'))
                    else:
                        flash('New Password Must Be Different Than Current Password')
                        return redirect(url_for('menu'))
                else:
                    flash('Incorrect Current Password')
                    return redirect(url_for('menu'))
            elif "startExistingGame" in request.form:
                game_id = request.form['existingGame']
                #add authentication here
                return redirect(url_for('game', game_id=game_id))
            elif "startGame" in request.form:
                opponent = request.form['opponent']
                date = datetime.now()
                new_game = Game(player1id=user.id,
                    player2id=opponent,
                    date=date,
                    b11 = '',
                    b21 = '',
                    b31 = '',
                    b41 = '',
                    b51 = '',
                    b61 = '',
                    b12 = '',
                    b22 = '',
                    b32 = '',
                    b42 = '',
                    b52 = '',
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
                    b65 = '',
                    b16 = '',
                    b26 = '',
                    b36 = '',
                    b46 = '',
                    b56 = '',
                    b66 = '',
                    previousGhost='none',
                    previousPlayer=0
                )
                session.add(new_game)
                session.commit()
                game_id = session.query(Game).filter_by(date=date).one().id
                return redirect(url_for('game', game_id=game_id))
    else:
        flash('Please log in')
        return render_template('login.html')



@app.route('/game/<int:game_id>/', methods=['GET', 'POST'])
def game(game_id):
    ghostList = ['p1b1','p1b2','p1b3','p1b4','p1y1','p1y2','p1y3','p1y4','p2b1','p2b2','p2b3','p2b4','p2y1','p2y2','p2y3','p2y4']
    deadGhosts = ['p1b1','p1b2','p1b3','p1b4','p1y1','p1y2','p1y3','p1y4','p2b1','p2b2','p2b3','p2b4','p2y1','p2y2','p2y3','p2y4']
    locationList = ['b11','b21','b31','b41','b51','b61','b12','b22','b32','b42','b52','b62','b13','b23','b33','b43','b53','b63','b14','b24','b34','b44','b54','b64','b15','b25','b35','b45','b55','b65','b16','b26','b36','b46','b56','b66']
    if 'username' in login_session:
        users = session.query(User)
        users = users.order_by(User.name.asc())
        user = users.filter_by(name=login_session['username']).one()
        userid = user.id
        userNotification = user.notifications
        game = session.query(Game).filter(Game.id==game_id).one()
        print "previous player " + str(game.previousPlayer)
        if user.id == game.player1id:
            opponent = users.filter_by(id=game.player2id).one()
            opponentPlayer = 2
            startingVal = 20
            opponentStartingVal = 10
            userPlayer = 1
        elif user.id == game.player2id:
            opponent = users.filter_by(id=game.player1id).one()
            opponentPlayer = 1
            startingVal = 10
            opponentStartingVal = 20
            userPlayer = 2
        else:
            flash('You Are Not Part Of This Game')
            return redirect(url_for('menu'))
        for ghost in ghostList:
            if ghost == game.b11:
                deadGhosts.remove(ghost)
            elif ghost == game.b21:
                deadGhosts.remove(ghost)
            elif ghost == game.b31:
                deadGhosts.remove(ghost)
            elif ghost == game.b41:
                deadGhosts.remove(ghost)
            elif ghost == game.b51:
                deadGhosts.remove(ghost)
            elif ghost == game.b61:
                deadGhosts.remove(ghost)
            elif ghost == game.b12:
                deadGhosts.remove(ghost)
            elif ghost == game.b22:
                deadGhosts.remove(ghost)
            elif ghost == game.b32:
                deadGhosts.remove(ghost)
            elif ghost == game.b42:
                deadGhosts.remove(ghost)
            elif ghost == game.b52:
                deadGhosts.remove(ghost)
            elif ghost == game.b62:
                deadGhosts.remove(ghost)
            elif ghost == game.b13:
                deadGhosts.remove(ghost)
            elif ghost == game.b23:
                deadGhosts.remove(ghost)
            elif ghost == game.b33:
                deadGhosts.remove(ghost)
            elif ghost == game.b43:
                deadGhosts.remove(ghost)
            elif ghost == game.b53:
                deadGhosts.remove(ghost)
            elif ghost == game.b63:
                deadGhosts.remove(ghost)
            elif ghost == game.b14:
                deadGhosts.remove(ghost)
            elif ghost == game.b24:
                deadGhosts.remove(ghost)
            elif ghost == game.b34:
                deadGhosts.remove(ghost)
            elif ghost == game.b44:
                deadGhosts.remove(ghost)
            elif ghost == game.b54:
                deadGhosts.remove(ghost)
            elif ghost == game.b64:
                deadGhosts.remove(ghost)
            elif ghost == game.b15:
                deadGhosts.remove(ghost)
            elif ghost == game.b25:
                deadGhosts.remove(ghost)
            elif ghost == game.b35:
                deadGhosts.remove(ghost)
            elif ghost == game.b45:
                deadGhosts.remove(ghost)
            elif ghost == game.b55:
                deadGhosts.remove(ghost)
            elif ghost == game.b65:
                deadGhosts.remove(ghost)
            elif ghost == game.b16:
                deadGhosts.remove(ghost)
            elif ghost == game.b26:
                deadGhosts.remove(ghost)
            elif ghost == game.b36:
                deadGhosts.remove(ghost)
            elif ghost == game.b46:
                deadGhosts.remove(ghost)
            elif ghost == game.b56:
                deadGhosts.remove(ghost)
            elif ghost == game.b66:
                deadGhosts.remove(ghost)
        userDeadBlue = 0
        userDeadYellow = 0
        opponentDeadBlue = 0
        opponentDeadYellow = 0
        for ghost in deadGhosts:
            if ghost[1] == str(userPlayer) and ghost[2] == 'b':
                userDeadBlue +=1
            elif ghost[1] == str(userPlayer) and ghost[2] == 'y':
                userDeadYellow +=1
            elif ghost[1] == str(opponentPlayer) and ghost[2] == 'b':
                opponentDeadBlue +=1
            elif ghost[1] == str(opponentPlayer) and ghost[2] == 'y':
                opponentDeadYellow +=1
        if game.previousPlayer == 0 or game.previousPlayer > 2:
            winner = ''
            wonBy = ''
        else:
            print "here"
            print game.b66
            print game.b66[1:3]
            if userDeadYellow == 4:
                wonBy = "yellow"
                winner = userPlayer
            elif userDeadBlue == 4:
                wonBy = "blue"
                winner = opponentPlayer
            elif opponentDeadYellow == 4:
                wonBy = "yellow"
                winner = opponentPlayer
            elif userDeadBlue == 4:
                wonBy = "blue"
                winner = opponentPlayer
            elif (game.b11[1:2] == "1b" or game.b61[1:3] == "1b") and game.previousPlayer == 2:
                wonBy = "exit"
                winner = 1
            elif (game.b16[1:2] == "2b" or game.b66[1:3] == "2b") and game.previousPlayer == 1:
                wonBy = "exit"
                winner = 2
            else:
                winner = ''
                wonBy = ''
        if request.method == 'GET':
            if game.previousPlayer == userPlayer or game.previousPlayer == userPlayer * 10:
                flash("Waiting for Opponent's Move, Please Check Back Later")
            return render_template('board.html',
                                    playerUsername=login_session['username'],
                                    userid=user.id,
                                    users=users,
                                    userNotification=userNotification,
                                    game=game,
                                    userPlayer=userPlayer,
                                    startingVal=startingVal,
                                    opponentStartingVal=opponentStartingVal,
                                    opponent=opponent,
                                    deadGhosts=deadGhosts,
                                    winner=winner,
                                    wonBy=wonBy)
        elif request.method == 'POST':
            rawMoves = request.form['moves']
            #ghost : location
            moveDict = ast.literal_eval(rawMoves)
            dead = request.form['dead']
            originalLocation = request.form['originalLocation']
            moveID = request.form['playerID']
            if moveID == str(userid):
                for move in moveDict:
                    if game.previousPlayer == 1 or game.previousPlayer == 2:
                        exec("game.%s = ''") % (originalLocation)
                    exec("game.%s = move" % (moveDict[move]))
                    game.previousGhost = move
                game.date = datetime.now()
                if game.previousPlayer == 1:
                    game.previousPlayer = 2
                elif game.previousPlayer == 2:
                    game.previousPlayer = 1
                else:
                    game.previousPlayer = game.previousPlayer + userPlayer*10
                    if game.previousPlayer == 30:
                        game.previousPlayer = 2
                session.add(game)
                session.commit()
                if game.previousPlayer == userPlayer or game.previousPlayer == userPlayer * 10:
                    flash("Waiting for Opponent's Move, Please Check Back Later")
                return render_template('board.html',
                                        playerUsername=login_session['username'],
                                        userid=user.id,
                                        users=users,
                                        userNotification=userNotification,
                                        game=game,
                                        userPlayer=userPlayer,
                                        startingVal=startingVal,
                                        opponentStartingVal=opponentStartingVal,
                                        opponent=opponent,
                                        deadGhosts=deadGhosts,
                                        winner=winner,
                                        wonBy=wonBy)
            else:
                flash('ID Match Error, Please Try Again')
                return redirect(url_for('game', game_id=game_id))
    else:
        flash('Please log in')
        return render_template('login.html')




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
