
from flask import Blueprint, request, jsonify
from services.helper import *
import firebase_admin, os, requests, random
from firebase_admin import credentials, db
from translate import Translator
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from collections import deque

ai_blueprint = Blueprint('ai', __name__)

# Initialize Firebase !!!! PALITAN YUNG  FILE PATH !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! v v v v
cred = credentials.Certificate(r'C:\Users\franz\vscode\gam\gamified-en-to-ilo-translator\ai-database-a2089-firebase-adminsdk-bogd7-808afea2db.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ai-database-a2089-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Get a reference to the Firebase Realtime Database
ref = db.reference()

#Define path to models
EN_ILO_MODEL_DIRECTORY = 'models/opus-mt-ilo-en'
ILO_EN_MODEL_DIRECTORY = 'models/opus-mt-en-ilo'
RANDOM_WORD_API_URL = ' https://random-word-form.herokuapp.com/random/noun?count=4'

translator = Translator(to_lang='ilo', model_path=EN_ILO_MODEL_DIRECTORY)

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
    

# Flask routes...


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

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Initialize DQN agent
state_size = 4  # Number of words
action_size = 3  # Number of choices (excluding correct answer)
agent = DQNAgent(state_size, action_size)