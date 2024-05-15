
from flask import Blueprint, request, jsonify
from services.helper import *
import firebase_admin, os, requests, random
from firebase_admin import credentials, db
import numpy as np
from services.DQNAagent import *
from concurrent.futures import ThreadPoolExecutor
from flask import session, render_template
from firebase_handler import *


ai_blueprint = Blueprint('ai', __name__)

#Define path to models
EN_ILO_MODEL_DIRECTORY = 'models/opus-mt-ilo-en'
ILO_EN_MODEL_DIRECTORY = 'models/opus-mt-en-ilo'
RANDOM_WORD_API_URL = ' https://random-word-form.herokuapp.com/random/noun?count=4'
translator = Translator(to_lang='ilo', model_path=EN_ILO_MODEL_DIRECTORY)


@ai_blueprint.route('/')
def index():
    return render_template('login.html')


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

    authentication_result = authenticate_user(username, password)
    return authentication_result, 200, {'Content-Type': 'application/json'}

@ai_blueprint.route('/submitanswer', methods=['POST'])
def submitanswer():
    data = request.json
    selected_translation = data.get('selectedTranslation')
    is_correct = data.get('isCorrect')

    # Handle correct or incorrect answer
    if is_correct:
        # Handle correct answer
        pass
    else:
        # Handle incorrect answer
        pass

    # Fetch new word based on the difficulty level
    difficulty_level = get_difficulty_level(selected_translation)
    if difficulty_level:
        words = get_random_words(difficulty_level)
        if words:
            correct_word = words[0]
            translation_choices = words[1:]
            state = np.array([get_word_embeddings(word) for word in translation_choices])
            action = agent.act(state)
            chosen_word = translation_choices[action]
            correct_translation = translator.translate(correct_word)

            with ThreadPoolExecutor() as executor:
                choices = list(executor.map(translate_word, words))

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
    else:
        return jsonify({"error": "no difficulty l"})

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

