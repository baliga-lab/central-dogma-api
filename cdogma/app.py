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
    #password = payload['password']
  except:
    return jsonify(status="error", error="Please provide a user name")

  conn = dbconn()
  cur = conn.cursor()
  try:
    cur.execute('select id from users where name=%s', [username])
    row = cur.fetchone()
    if row is None:
      cur.execute('insert into users (name) values (%s)', [username])
      conn.commit()
    access_token = create_access_token(identity=payload['username'])
    return jsonify(status="ok", access_token=access_token)
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
  payload = request.get_json()
  conn = dbconn()
  cur = conn.cursor()
  try:
    score = payload['score']
    try:
      session_code = payload['session_code']
      cur.execute('select id from game_sessions where code=%s', [session_code])
      session_id = cur.fetchone()[0]
    except:
      session_id = None
    current_user = get_jwt_identity()
    cur.execute('select id from users where name=%s', [current_user])
    user_id = cur.fetchone()[0]
    if session_id is None:
      cur.execute('insert into user_game_log (user_id,level_id,score) values (%s,%s,%s)',
                  [user_id, level_id, score])
    else:
      cur.execute('insert into user_game_log (user_id,level_id,score,session_id) values (%s,%s,%s,%s)',
                  [user_id, level_id, score, session_id])
    conn.commit()
    return jsonify(status="ok")
  except:
    traceback.print_exc()
    return jsonify(status="error", error="unknown error")
  finally:
    if cur is not None:
      cur.close()


@app.route('/leveldata/<level_id>', methods=["POST"])
@jwt_required
def level_completion_data(level_id):
  """passing in the level id, the score, and optional session id
  submit the level complete and log down the level scores and stuff"""
  payload = request.get_json()
  conn = dbconn()
  cur = conn.cursor()
  try:
    try:
      session_code = payload['session_code']
      cur.execute('select id from game_sessions where code=%s', [session_code])
      session_id = cur.fetchone()[0]
    except:
      session_id = None
    current_user = get_jwt_identity()
    cur.execute('select id from users where name=%s', [current_user])
    user_id = cur.fetchone()[0]
    if session_id is not None:
      cur.execute('select score from user_game_log where user_id=%s and level_id=%s and session_id=%s',
                  [user_id, level_id, session_id])
    else:
      cur.execute('select score from user_game_log where user_id=%s and session_id is null and level_id=%s',
                  [user_id, level_id])
    row = cur.fetchone()
    if row is not None:
      result = {'score': row[0]}
    else:
      result = {'score': 0}
    return jsonify(status="ok", result=result)
  except:
    traceback.print_exc()
    return jsonify(status="error", error="unknown error")
  finally:
    if cur is not None:
      cur.close()


@app.route('/game_rt/<level_id>', methods=["POST"])
def log_level_completion_retreat(level_id):
  """passing in the level id, the score, and optional session id
  submit the level complete and log down the level scores and stuff
  This does not require login and was only created for the ISB retreat
  """
  payload = request.get_json()
  conn = dbconn()
  cur = conn.cursor()
  try:
    current_user = payload['user']
    score = payload['score']
    accuracy = payload['accuracy']
    try:
      session_code = payload['session_code']
      cur.execute('select id from game_sessions where code=%s', [session_code])
      session_id = cur.fetchone()[0]
    except:
      session_id = None
    cur.execute('select id from users where name=%s', [current_user])
    row = cur.fetchone()
    if row is None:
      cur.execute('insert into users (name) values (%s)', [current_user] )
      user_id = cur.lastrowid
    else:
      user_id = row[0]
    if session_id is not None:
      # only log to valid session
      cur.execute('insert into user_game_log (user_id,level_id,score,accuracy,session_id) values (%s,%s,%s,%s,%s)',
                  [user_id, level_id, score, accuracy, session_id])
      conn.commit()
    return jsonify(status="ok")
  except:
    traceback.print_exc()
    return jsonify(status="error", error="unknown error")
  finally:
    if cur is not None:
      cur.close()


@app.route('/response/<question_id>', methods=["POST"])
@jwt_required
def log_question_response(question_id):
  """passing in the question id, answer option, correctness, and session id
  logs down the flashcard question answered and whether it is correct or not"""
  payload = request.get_json()
  conn = dbconn()
  cur = conn.cursor()
  try:
    answer_option = payload['answer_option']
    correctness = payload['correctness']
    if 'session_code' in payload:
      session_code = payload['session_code']
      cur.execute('select id from game_sessions where code=%s', [session_code])
      session_id = cur.fetchone()[0]
    else:
      session_id = None

    current_user = get_jwt_identity()
    cur.execute('select id from users where name=%s', [current_user])
    user_id = cur.fetchone()[0]

    if session_id is None:
      cur.execute('insert into user_question_log (user_id,answer_option,correctness) values (%s,%s,%s)',
                  [user_id, answer_option, correctness])
    else:
      cur.execute('insert into user_question_log (user_id,answer_option,correctness,session_id) values (%s,%s,%s,%s)',
                  [user_id, answer_option, correctness, session_id])

    conn.commit()

    return jsonify(status="ok")
  except:
    traceback.print_exc()
    return jsonify(status="error", error="unknown error")


@app.route('/game', methods=["GET"])
@jwt_required
def game_completion():
  """lists all the games/levels the user has completed"""
  conn = dbconn()
  cur = conn.cursor()
  try:
    current_user = get_jwt_identity()
    cur.execute('select s.code,level_id,score from user_game_log ugl join users u on ugl.user_id=u.id left outer join game_sessions s on ugl.session_id=s.id where u.name=%s',
                [current_user])
    entries = [{'session_code': '' if session_code is None else session_code,
                'level_id': level_id,
                'score': score} for session_code, level_id, score in cur.fetchall()]
    return jsonify(status="ok", entries=entries)
  except:
    traceback.print_exc()
    return jsonify(status="error", error="unknown error")
  finally:
    if cur is not None:
      cur.close()


"""
Leaderboard functions
"""

@app.route('/leaderboard', methods=["POST"])
def get_all_time_leaderboard():
  payload = request.get_json()
  try:
    orderby = payload['orderby']
  except:
    orderby = 'score'

  conn = dbconn()
  cur = conn.cursor()
  try:
    q = 'select u.name,ugl.score from user_game_log ugl join users u on ugl.user_id=u.id '
    if orderby == 'name':
      q += 'order by u.name desc'
    else:
      q += 'order by ugl.score desc'
    cur.execute(q)
    leaders = [{'username': username, 'score': score} for username, score in cur.fetchall()]
    return jsonify(status='ok', entries=leaders)
  except:
    traceback.print_exc()
    return jsonify(status='error', error="unknown error")
  finally:
    if cur is not None:
      cur.close()


@app.route('/leaderboard/<session_id>', methods=["POST"])
def get_session_leaderboard(session_id):
  payload = request.get_json()
  try:
    orderby = payload['orderby']
  except:
    orderby = 'score'

  conn = dbconn()
  cur = conn.cursor()
  try:
    q = 'select u.name,ugl.score from user_game_log ugl join users u on ugl.user_id=u.id join game_sessions s on ugl.session_id=s.id where s.code=%s '
    if orderby == 'name':
      q += 'order by u.name desc'
    else:
      q += 'order by ugl.score desc'

    cur.execute(q, [session_id])
    leaders = [{'username': username, 'score': score} for username, score in cur.fetchall()]
    return jsonify(status='ok', entries=leaders)
  except:
    traceback.print_exc()
    return jsonify(status='error', error="unknown error")
  finally:
    if cur is not None:
      cur.close()


@app.route('/level_leaderboard/<level_id>', methods=["POST"])
def global_level_leaderboard(level_id):
  payload = request.get_json()
  try:
    orderby = payload['orderby']
  except:
    orderby = 'score'

  conn = dbconn()
  cur = conn.cursor()
  try:
    q = 'select u.name,ugl.score from user_game_log ugl join users u on ugl.user_id=u.id where level_id=%s'
    if orderby == 'name':
      q += 'order by u.name desc'
    else:
      q += 'order by ugl.score desc'
    cur.execute(q, [level_id])
    leaders = [{'username': username, 'score': score} for username, score in cur.fetchall()]
    return jsonify(status='ok', entries=leaders)
  except:
    traceback.print_exc()
    return jsonify(status='error', error="unknown error")
  finally:
    if cur is not None:
      cur.close()


@app.route('/level_leaderboard/<session_id>/<level_id>', methods=["POST"])
def level_session_leaderboard(session_id, level_id):
  payload = request.get_json()
  try:
    orderby = payload['orderby']
  except:
    orderby = 'score'

  conn = dbconn()
  cur = conn.cursor()
  try:
    q = 'select u.name,ugl.score from user_game_log ugl join users u on ugl.user_id=u.id join game_sessions s on ugl.session_id=s.id where s.code=%s and level_id=%s '
    if orderby == 'name':
      q += 'order by u.name desc'
    else:
      q += 'order by ugl.score desc'

    cur.execute(q, [session_id, level_id])
    leaders = [{'username': username, 'score': score} for username, score in cur.fetchall()]
    return jsonify(status='ok', entries=leaders)
  except:
    traceback.print_exc()
    return jsonify(status='error', error="unknown error")
  finally:
    if cur is not None:
      cur.close()


"""
Link tracking
"""

@app.route('/tracklink', methods=["POST"])
@jwt_required
def track_link():
  """
  - passing in the session code, start and end
  - ensures that the code does not exist before creating a session with those info
  """
  payload = request.get_json()
  conn = dbconn()
  cur = conn.cursor()
  try:
    url = payload['url']
    current_user = get_jwt_identity()
    cur.execute('select id from users where name=%s', [current_user])
    user_id = cur.fetchone()[0]
    cur.execute('insert into hyperlink_log (user_id,url) values (%s,%s)', [user_id, url])
    conn.commit()
  except:
    traceback.print_exc()
    return jsonify(status="error", error="unknown error")
  finally:
    if cur is not None:
      cur.close()

  return jsonify(status="ok")


"""
NEW JOSH API
"""

@app.route('/user/signin', methods=["POST"])
def signin_user():
  """passing in the username and session id
  login the user and returns a session token that all other endpoints can use"""
  payload = request.get_json()
  gender = None
  state = None
  grade = None
  try:
    username = payload['username']
    session_id = payload['session_id']
    userinfo = payload['userinfo']
    try:
      gender = userinfo['gender']
    except:
      print('no gender provided')
    try:
      grade = userinfo['grade']
    except:
      print('no grade provided')
    try:
      state = userinfo['state']
    except:
      print('no state provided')

  except:
    return jsonify(status="error", error="Please provide a user name")

  print("signin_user(), user: %s session: %s" % (username, session_id))
  conn = dbconn()
  cur = conn.cursor()
  try:
    cur.execute('select id from users where name=%s', [username])
    row = cur.fetchone()
    if row is None:
      cur.execute('insert into users (name,gender2,state2,grade2) values (%s,%s,%s,%s)',
                  [username, gender, state, grade])
      conn.commit()
    access_token = create_access_token(identity=payload['username'])
    return jsonify(status="ok", access_token=access_token)
  except:
    traceback.print_exc()
    return jsonify(status="error", error="unknown error")
  finally:
    if cur is not None:
      cur.close()


@app.route('/user/storevar', methods=["POST"])
@jwt_required
def store_variable():
  """store global variable"""
  payload = request.get_json()
  conn = dbconn()
  cur = conn.cursor()
  try:
    current_user = get_jwt_identity()
    cur.execute('select id from users where name=%s', [current_user])
    user_id = cur.fetchone()[0]
    session_id = payload['session_id']
    cur.execute('select id from game_sessions where code=%s', [session_id])
    row = cur.fetchone()
    if row is not None:
      session_pk = row[0]
    else:
      # use default session if session code not found
      session_pk = 1

    TIME_FORMAT = '%m/%d/%Y, %I:%M:%S %p'
    global_var = payload['global']
    level_performance = global_var['LEVEL_PERFORMANCE']
    for lp in level_performance:
      """{u'levelNum': 1, u'missed': 12, u'level': 1, u'process': u'dna replication', u'timestamp': u'Mon Mar 16 2020 11:02:32 GMT-0700 (Pacific Daylight Time)', u'correct': 3, u'error': 0, u'total': 15, u'speed': 42, u'lvlType': u'dna_replication', u'rotateNT': False}"""
      print(lp)
      levelnum = lp['levelNum']
      missed = lp['missed']
      level = lp['level']
      process = lp['process']  # dna replicaion etc
      timestamp = lp['timestamp']
      num_correct = lp['correct']
      num_error = lp['error']
      num_total = lp['total']
      speed = lp['speed']
      level_type = lp['lvlType']
      rotational = lp['rotateNT']
      score = lp['score']
      # '3/16/2020, 4:06:58 PM'
      finished_at = datetime.datetime.strptime(timestamp, TIME_FORMAT)
      print(finished_at)
      cur.execute('select id from level_types where name=%s', [level_type])
      level_type_id = cur.fetchone()[0]
      cur.execute('select id from processes where name=%s', [process])
      process_id = cur.fetchone()[0]
      cur.execute('insert into levels (finished_at,level,process,level_type,speed,rotational,missed,correct,num_errors,num_total,level_num,session_id,user_id,score) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                  [finished_at, level, process_id, level_type_id, speed, rotational, missed,
                   num_correct, num_error, num_total, levelnum, session_pk, user_id, score])
    conn.commit()

    quiz_result = global_var['QUIZ_RESULTS']
    for qr in quiz_result:
      timestamp = qr['timestamp']
      finished_at = datetime.datetime.strptime(timestamp, TIME_FORMAT)
      score = qr['score']
      print("finished at: ", finished_at)
      print("Score: ", score)
      num_attempts = qr['attempts']
      q = qr['question']
      correct_option = q['correct']
      prompt = q['prompt']
      qtype = q['type']  # multiple choice or drag and drop
      worth = q['worth']
      options = q['options']
      question_num = qr['questionNum']  # the question ID
      cur.execute('select id from questions where game_session_id=%s and prompt=%s', [session_pk, prompt])
      row = cur.fetchone()
      if row is None:
        cur.execute('select id from question_types where name=%s', [qtype])
        qtype_pk = cur.fetchone()[0]
        cur.execute('insert into questions (question_type,worth,prompt,correct_option,game_session_id) values (%s,%s,%s,%s,%s)',
                    [qtype_pk, worth, prompt, correct_option, session_pk])
        question_pk = cur.lastrowid
        print("insert new question with id: %d !!!!" % question_pk)
        for index, opt in enumerate(options):
          cur.execute('insert into question_options (question_id,content,option_num) values (%s,%s,%s)',
                      [question_pk, opt, index + 1])
        conn.commit()
      else:
        question_pk = row[0]
        print("question found id: %d !!!" % question_pk)
        cur.execute('insert into quiz_results (answered_at,question_id,attempts,num_questions_asked,score,user_id) values (%s,%s,%s,%s,%s,%s)',
                  [finished_at, question_pk, num_attempts, question_num, score, user_id])
      conn.commit()

    # Ignore for now
    score = global_var['SCORE']
    active_education = global_var['ACTIVE_EDUCATION']
    active_effects = global_var['ACTIVE_EFFECTS']
    print(global_var)
    return jsonify(status="ok")
  except:
    traceback.print_exc()
    return jsonify(status="error", error="no parameters")
  finally:
    if cur:
      cur.close()


@app.route('/total_leaderboard', methods=["POST"])
def get_total_leaderboard():
  payload = request.get_json()
  num_rows = 10
  session_id = payload['session_id']
  try:
    # orderby should be "levelScore" and "quizScore", support "score", for legacy reasons
    orderby = payload['orderby']
  except:
    orderby = 'score'

  conn = dbconn()
  try:
    cur = conn.cursor()
    cur.execute('select id from game_sessions where code=%s', [session_id])

    row = cur.fetchone()
    if row is not None:
      session_pk = row[0]
    else:
      # Use default session if provided session not found
      session_pk = 1

    if orderby == 'quizScore':
      q = 'select u.name as username,sum(score) as quiz_score from quiz_results qr join users u on qr.user_id=u.id join questions q on q.id=qr.question_id where game_session_id=%s group by username,question_id order by quiz_score desc'
    else:
      q = 'select u.name,score from levels l join users u on l.user_id=u.id where session_id=%s order by score desc'
    cur.execute(q, [session_pk])
    result = [{"userName": "-".join(uname.split('-')[:3]), "value": int(score)} for uname, score in cur.fetchall()]
    return jsonify(status="ok", result=result)
  except:
    traceback.print_exc()
  finally:
    if cur is not None:
      cur.close()


@app.route('/level_leaderboard', methods=["POST"])
def get_level_leaderboard():
  payload = request.get_json()
  session_id = payload['session_id']
  level = payload['level']
  num_rows = 10
  try:
    num_rows = payload['numrows']
  except:
    pass

  conn = dbconn()
  cur = conn.cursor()
  try:
    cur.execute('select id from game_sessions where code=%s', [session_id])
    row = cur.fetchone()
    if row is not None:
      session_pk = row[0]
    else:
      # use default session if not found
      session_pk = 1

    q = 'select u.name, score from levels l join users u on l.user_id=u.id where session_id=%s and level=%s order by score'
    cur.execute(q, [session_pk, level])
    result = [{"userName": "-".join(uname.split('-')[:3]), "value": score} for uname, score in cur.fetchall()]
    return jsonify(status="ok", result=result)
  except:
    traceback.print_exc()
    return jsonify(status="error", result=[])
  finally:
    if cur is not None:
      cur.close()



if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'trststrtsrtgprestnorgp654g'
    app.run(host='0.0.0.0', debug=True)
