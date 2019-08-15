#!/usr/bin/env python

import logging
import json
import os
import traceback
from collections import defaultdict
import MySQLdb

from flask import Flask, Response, url_for, redirect, render_template, request, session, flash, jsonify, g
import flask
from flask_cors import CORS, cross_origin

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

import datetime
import requests
import users
import traceback

app = Flask(__name__)
CORS(app)

app.config.from_envvar('APP_SETTINGS')

jwt = JWTManager(app)

def dbconn():
  if not hasattr(g, 'dbconn'):
    g.dbconn = MySQLdb.connect(user=app.config['DATABASE_USER'],
                               passwd=app.config['DATABASE_PASSWORD'],
                               db=app.config['DATABASE_NAME'],
                               use_unicode=True, charset="utf8")
  return g.dbconn


@app.teardown_appcontext
def close_db(error):
  if hasattr(g, 'dbconn'):
    g.dbconn.close()


@app.route('/info')
def info():
    return jsonify(status="ok")


@app.route('/user/register', methods=["POST"])
def register_user():
  """passing in the username, password, grade, gender.
  make a user and gives a session token that all other endpoints can use"""
  payload = request.get_json()
  conn = dbconn()
  cur = conn.cursor()
  try:
    username = payload['username']
    password = payload['password']
    grade = payload['grade']
    gender = payload['gender']
    cur.execute('select count(*) from users where name=%s', [username])
    if cur.fetchone()[0] > 0:
      return jsonify(status="error", error="user name already exists")

    salt, hashval = users.make_password(password)

    cur.execute('insert into users (name,grade,gender,hash,salt) values (%s,%s,%s,%s,%s)',
                [username, grade, gender, hashval, salt])
    conn.commit()
    access_token = create_access_token(identity='mockuser')
    return jsonify(status="ok", access_token=access_token)
  except Exception as e:
    traceback.print_exc()
    return jsonify(status="error", error="unknown error")
  finally:
    # It looks like we can not close cur automatically in a "with" statement using
    # MySQLDb and Python2
    if cur is not None:
      cur.close()


@app.route('/user/login', methods=["POST"])
def login_user():
  """passing in the username and password
  login the user and returns a session token that all other endpoints can use"""
  payload = request.get_json()
  try:
    username = payload['username']
    password = payload['password']
  except:
    return jsonify(status="error", error="Please provide a user name and password")

  conn = dbconn()
  cur = conn.cursor()
  try:
    cur.execute('select hash, salt from users where name=%s', [username])
    row = cur.fetchone()
    if row is not None:
      hashval, salt = row
      if users.verify_password(password, salt, hashval):
        access_token = create_access_token(identity=payload['username'])
        return jsonify(status="ok", access_token=access_token)
      else:
        return jsonify(status="error", error="invalid password")
  except:
    traceback.print_exc()
    return jsonify(status="error", error="unknown error")
  finally:
    if cur is not None:
      cur.close()


"""
Session functions
"""
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

@app.route('/session', methods=["POST"])
@jwt_required
def make_session():
  """
  - passing in the session code, start and end
  - ensures that the code does not exist before creating a session with those info
  """
  payload = request.get_json()
  conn = dbconn()
  cur = conn.cursor()
  try:
    session_code = payload['session_code']
    start_time_str = payload['start_time']
    end_time_str = payload['end_time']

    start_time = datetime.datetime.strptime(start_time_str, DATE_FORMAT)
    end_time = datetime.datetime.strptime(end_time_str, DATE_FORMAT)
    cur.execute('select count(*) from game_sessions where code=%s', [session_code])
    if cur.fetchone()[0] > 0:
      return jsonify(status="error", error="a session with code '%s' already exists" % session_code)
    else:
      current_user = get_jwt_identity()
      cur.execute('select id from users where name=%s', [current_user])
      user_id = cur.fetchone()[0]
      cur.execute('insert into game_sessions (code,start_time,end_time,owner_id) values (%s,%s,%s,%s)',
                  [session_code, start_time, end_time, user_id])
      conn.commit()
  except:
    traceback.print_exc()
    return jsonify(status="error", error="unknown error")
  finally:
    if cur is not None:
      cur.close()

  return jsonify(status="ok")

def format_time(time_obj):
  return str(time_obj)


@app.route('/session', methods=["GET"])
@jwt_required
def owned_sessions():
  """
  gets the list of sessions that they "own" and can modify
  """
  conn = dbconn()
  cur = conn.cursor()
  try:
    current_user = get_jwt_identity()
    cur.execute('select code,start_time,end_time from game_sessions gs join users u on gs.owner_id=u.id where u.name=%s', [current_user])
    sessions = [{"session_code": code, "start_time": format_time(start_time),
                 "end_time": format_time(end_time)}
                for code, start_time, end_time in cur.fetchall()]
    return jsonify(status="ok", sessions=sessions)
  except:
    traceback.print_exc()
    return jsonify(status="error", error="unknown error")
  finally:
    if cur is not None:
      cur.close()


@app.route('/session/<code>', methods=["GET"])
@jwt_required
def session_info(code):
  """passing in the session code
  returns the session information (start and end dates)"""
  conn = dbconn()
  cur = conn.cursor()
  try:
    cur.execute("select start_time, end_time from game_sessions where code=%s", [code])
    start_time, end_time = cur.fetchone()
    return jsonify(status="ok", session_info={"session_code": code,
                                              "start_time": format_time(start_time),
                                              "end_time": format_time(end_time)})
  except:
    traceback.print_exc()
    return jsonify(status="error", error="unknown error")
  finally:
    if cur is not None:
      cur.close()


@app.route('/session/<code>', methods=["PATCH"])
@jwt_required
def modify_session_info(code):
  """passing in the session code, start, and end
  modify session start and end times"""
  payload = request.get_json()
  conn = dbconn()
  cur = conn.cursor()
  try:
    start_time_str = payload['start_time']
    end_time_str = payload['end_time']
    start_time = datetime.datetime.strptime(start_time_str, DATE_FORMAT)
    end_time = datetime.datetime.strptime(end_time_str, DATE_FORMAT)

    cur.execute('select count(*) from game_sessions where code=%s', [code])
    if cur.fetchone()[0] == 0:
      return jsonify(status="error", error="session '%s' does not exist" % code)
    cur.execute('update game_sessions set start_time=%s, end_time=%s where code=%s',
                [start_time, end_time, code])
    conn.commit()
    return jsonify(status="ok")
  except:
    return jsonify(status="error", error="unknown error")
  finally:
    if cur is not None:
      cur.close()


"""
Game functions
"""

@app.route('/game/<level_id>', methods=["POST"])
@jwt_required
def log_level_completion(level_id):
  """passing in the level id, the score, and optional session id
  submit the level complete and log down the level scores and stuff"""
  return jsonify()


@app.route('/response/<question_id>', methods=["POST"])
@jwt_required
def log_question_response(level_id):
  """passing in the question id, answer option, correctness, and session id
  logs down the flashcard question answered and whether it is correct or not"""
  return jsonify()


@app.route('/game', methods=["GET"])
@jwt_required
def completed_games():
  """lists all the games/levels the user has completed"""
  return jsonify()


"""
Leaderboard functions
"""

@app.route('/leaderboard', methods=["GET"])
def get_all_time_leaderboard():
  leaders = [
    {'username': 'xyz', 'score': 12345},
    {'username': 'abc', 'score': 12122}
  ]
  return jsonify(entries=leaders)


@app.route('/leaderboard/<session_id>', methods=["GET"])
def get_session_leaderboard(session_id):
  leaders = [
    {'username': 'xyz', 'score': 12345},
    {'username': 'abc', 'score': 12122}
  ]
  return jsonify(entries=leaders)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'trststrtsrtgprestnorgp654g'
    app.run(host='0.0.0.0', debug=True)
