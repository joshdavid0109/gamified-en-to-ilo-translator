
from flask import Blueprint, request, jsonify
from services.helper import *
import firebase_admin, os, requests, random
from firebase_admin import credentials, db
import numpy as np
# from services.DQNAagent import *
from concurrent.futures import ThreadPoolExecutor
from flask import session, render_template, url_for, redirect
from firebase_handler import *
import math
from math import log


ai_blueprint = Blueprint('ai', __name__)


@ai_blueprint.route('/')
def index():
    if 'userid' not in session:
        return render_template('login.html')
    print(session['userid'])
    print(session['username'])
    print(session['points'])
    return render_template('mainpage.html')


@ai_blueprint.route('/mainpage')
def main_page():
    return render_template('mainpage.html');


@ai_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "error": "Missing username or password"})

    authentication_result = json.loads(authenticate_user(username, password))
    if authentication_result.get('success'):
        session['userid'] = authentication_result['user_id']
        session['username'] = authentication_result['username']
        session['points'] = authentication_result['points']
        return jsonify({"success": True})
    return jsonify(authentication_result)

@ai_blueprint.route('/get_choices', methods=['GET'])
def get_choices():
    # data = request.json
    # difficulty = data.get('difficulty')
    # numofchoices = data.get('numofchoices')
    words = get_random_words('medium')
    correct_word = words[0]
    translation_choices = words[1:]

    correct_translation = translate_word(correct_word)
    print(correct_translation)
    with ThreadPoolExecutor() as executor:
        choices = list(executor.map(translate_word, words))
    choices.remove(correct_translation)
    random.shuffle(choices)
    choices.insert(random.randint(0, len(choices)), correct_translation)
    return jsonify({
                    "word": correct_word,
                    "correct_answer": correct_translation,
                    "choices": choices
                }), 200

@ai_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('ai.index'))

@ai_blueprint.route('/leaderboards')
def leaderboards():
    return render_template('leaderboard.html')

@ai_blueprint.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
    
@ai_blueprint.route('/gamepage')
def gamepage():
    return render_template('gamepage.html', session_variable=session.get('userid'))

# return poitns (+ or -)
@ai_blueprint.route('/submitanswer', methods=['POST'])
def submitanswer():
    data = request.json
    
    selected_translation = data.get("selectedTranslation", "")
    is_correct = data.get("isCorrect", "")
    userid = data.get("userId", "")

    score = calculate_score(selected_translation, is_correct)
    
    update_response_json = update_points(userid, score)  # This returns a JSON string
    update_response = json.loads(update_response_json)  # Parse JSON string to dictionary
    
    if update_response["success"]:
        return jsonify({"score": score, "points": update_response["points"], "tier": update_response["tier"]})
    else:
        return jsonify({"score": score, "error": update_response["error"]}), 400



@ai_blueprint.route('/user', methods=['GET', 'POST'])
def get_user():
    user_ref = ref.child('users').child("user0001")
    user = user_ref.get()
    return user

@ai_blueprint.route('/getuserid')
def get_userid():
    userid = session.get('userid')
    return jsonify({'userid': userid})

@ai_blueprint.route('/getpoints')
def get_points():
    points = session.get('points')
    return jsonify({'points': points})