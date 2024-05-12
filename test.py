from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin, os, requests, random
from firebase_admin import credentials, db
from translate import Translator
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np



app = Flask(__name__)
CORS(app, resources={r"/users": {"origins": "http://127.0.0.1:5500"}})
CORS(app, resources={r"/translate": {"origins": "http://127.0.0.1:5500"}})
CORS(app, resources={r"/easy": {"origins": "http://127.0.0.1:5500"}})
CORS(app, resources={r"/user": {"origins": "http://127.0.0.1:5500"}})
CORS(app, resources={r"": {"origins": "http://127.0.0.1:5500"}})


# Initialize Firebase
cred = credentials.Certificate(r'D:\flask_test\ai-database-a2089-firebase-adminsdk-bogd7-808afea2db.json')
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

# Helper function to get word embeddings (replace with actual implementation)
def get_word_embeddings(word):
    return np.random.rand(50)  # Example: random embeddings of size 50

# Get random words with different difficulty levels
def get_random_words(difficulty):
    if difficulty == 'easy':
        RANDOM_WORD_API_URL = 'https://random-word-form.herokuapp.com/random/noun?count=4'
    elif difficulty == 'medium':
        RANDOM_WORD_API_URL = 'https://random-word-form.herokuapp.com/random/noun?count=6'
    elif difficulty == 'hard':
        RANDOM_WORD_API_URL = 'https://random-word-form.herokuapp.com/random/noun?count=8'
    else:
        return None
    
    response = requests.get(RANDOM_WORD_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Flask routes...

with app.app_context():

    @app.route('/user', methods=['GET', 'POST'])
    def get_user():
        user_ref = ref.child('users').child("user0001")
        user = user_ref.get()
        return user
    
    @app.route('/easy', methods=['GET', 'POST'])
    def get_easy_word():
        return get_word('easy')

    @app.route('/medium', methods=['GET', 'POST'])
    def get_medium_word():
        return get_word('medium')

    @app.route('/hard', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/')
def index():
    return "test index"

# Define a route for '/users'
@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = ref.child('users').get()
        return jsonify(users), 200
    elif request.method == 'POST':
        data = request.get_json()
        # Process the data as needed
        return "Data received successfully", 200

# Define a route for /translate
@app.route('/translate', methods=['GET', 'POST'])
def translate():
    data = request.json
    print(data)
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Missing text field'}), 400

    translated_text = translator.translate(text)
    return jsonify({'translated_text': translated_text}), 200

if __name__ == '__main__':
    app.run(debug=True)
