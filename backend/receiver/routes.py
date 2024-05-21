
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
    return render_template('gamepage.html')

# return poitns (+ or -)
@ai_blueprint.route('/submitanswer', methods=['POST'])
def submitanswer():
    data = request.json
    
    selected_translation = data.get("selectedTranslation", "")
    is_correct = data.get("isCorrect", "").lower()
    
    score = calculate_score(selected_translation, is_correct)
    
    return jsonify({"score": score})



@ai_blueprint.route('/user', methods=['GET', 'POST'])
def get_user():
    user_ref = ref.child('users').child("user0001")
    user = user_ref.get()
    return user
    
@ai_blueprint.route('/easy', methods=['GET', 'POST'])
def get_easy_word():
    return get_word('easy')

@ai_blueprint.route('/medium', methods=['GET', 'POST'])
def get_medium_word():
    return get_word('medium')

@ai_blueprint.route('/hard', methods=['GET', 'POST'])
def get_hard_word():
    return get_word('hard')

def get_word(difficulty):
    words = get_random_words(difficulty)
    if words:
        correct_word = words[0]
        translation_choices = words[1:]
        state = np.array([get_word_embeddings(word) for word in translation_choices])
        action = agent.act(state)
        chosen_word = translation_choices[action]
        correct_translation = translator.translate(correct_word)
        choices = [translator.translate(word) for word in words]
        choices.remove(correct_translation)  # Remove correct translation from choices
        random.shuffle(choices)
        choices.insert(random.randint(0, len(choices)), correct_translation)  # Insert correct translation at random index
        reward = 1 if chosen_word == correct_word else 0
        agent.remember(state, action, reward, None, False)
        return jsonify({
            "word": correct_word,
            "correct_answer": correct_translation,
            "choices": choices
        }), 200
    else:
        return jsonify({"error": "Failed to fetch random words"}), 500
    


def get_difficulty_level(translation):
    # Logic to determine difficulty level based on translation
    # You can implement your logic here
    # For now, let's assume the translation length determines difficulty
    length = len(translation)
    if length <= 5:
        return 'easy'
    elif 5 < length <= 8:
        return 'medium'
    else:
        return 'hard'



# @ai_blueprint.route('/submitanswer', methods=['POST'])
# def submitanswer():
#     data = request.json
#     selected_translation = data.get('selectedTranslation')
#     is_correct = data.get('isCorrect')

#     # Handle correct or incorrect answer
#     if is_correct:
#         # Handle correct answer
#         pass
#     else:
#         # Handle incorrect answer
#         pass

#     # Fetch new word based on the difficulty level
#     difficulty_level = get_difficulty_level(selected_translation)
#     if difficulty_level:
#         words = get_random_words(difficulty_level)
#         if words:
#             correct_word = words[0]
#             translation_choices = words[1:]
#             state = np.array([get_word_embeddings(word) for word in translation_choices])
#             action = agent.act(state)
#             chosen_word = translation_choices[action]
#             correct_translation = translator.translate(correct_word)

#             with ThreadPoolExecutor() as executor:
#                 choices = list(executor.map(translate_word, words))

#             choices.remove(correct_translation)  # Remove correct translation from choices
#             random.shuffle(choices)
#             choices.insert(random.randint(0, len(choices)), correct_translation)  # Insert correct translation at random index
#             reward = 1 if chosen_word == correct_word else 0
#             agent.remember(state, action, reward, None, False)

#             return jsonify({
#                 "word": correct_word,
#                 "correct_answer": correct_translation,
#                 "choices": choices
#             }), 200
#         else:
#             return jsonify({"error": "Failed to fetch random words"}), 500
#     else:
#         return jsonify({"error": "no difficulty l"})