from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
from translate import Translator
# from googletrans import Translator # for google translate (does not support ilokano translation)
import os, requests
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM # ayaw sakin to


# from app import transformers_utils

app = Flask(__name__)
CORS(app, resources={r"/users": {"origins": "http://127.0.0.1:5500"}})
CORS(app, resources={r"/translate": {"origins": "http://127.0.0.1:5500"}})

# Initialize Firebase
cred = credentials.Certificate(r'D:\flask_test\ai-database-a2089-firebase-adminsdk-bogd7-808afea2db.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ai-database-a2089-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Get a reference to the Firebase Realtime Database
ref = db.reference()

# Initialize Google Translate API client
# translator = Translator()

#Define path to models
EN_ILO_MODEL_DIRECTORY = 'models/opus-mt-ilo-en'
ILO_EN_MODEL_DIRECTORY = 'models/opus-mt-en-ilo'
RANDOM_WORD_API_URL = 'https://random-word-api.herokuapp.com/all'

#load tokenizer and model
# en_ilo_tokenizer, en_ilo_model = transformers_utils.load_model_and_tokenizer(EN_ILO_MODEL_DIRECTORY)
# ilo_en_tokenizer, ilo_en_model = transformers_utils.load_model_and_tokenizer(ILO_EN_MODEL_DIRECTORY)

translator = Translator(to_lang='ilo', model_path=EN_ILO_MODEL_DIRECTORY)

def get_random_word():
    # Make a GET request to the random word API endpoint
    response = requests.get(RANDOM_WORD_API_URL)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the random word from the response
        random_word = data.get('word')

        return random_word
    else:
        # If the request was not successful, return None
        return None


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

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    data = request.json
    print(data)
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Missing text field'}), 400

    translated_text = translator.translate(text)
    return jsonify({'translated_text': translated_text}), 200

# Function to perform translation using the loaded model
def translate_text(text, target_language):
    if target_language == 'en':
        tokenizer = en_ilo_tokenizer
        model = en_ilo_model
    elif target_language == 'ilo':
        tokenizer = ilo_en_tokenizer
        model = ilo_en_model
    else:
        return "Invalid target language"

    input_ids = tokenizer(text, return_tensors="pt")["input_ids"]
    generated_sequence = model.generate(input_ids=input_ids)[0].numpy().tolist()
    translated_text = tokenizer.decode(generated_sequence, skip_special_tokens=True)
    return translated_text


if __name__ == '__main__':
    app.run(debug=True)
