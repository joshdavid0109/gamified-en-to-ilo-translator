import firebase_admin, os, random, requests
import numpy as np
from translate import Translator
import random

EN_ILO_MODEL_DIRECTORY = '../models/opus-mt-ilo-en'
ILO_EN_MODEL_DIRECTORY = '../models/opus-mt-en-ilo'
FINE_ILO_EN_MODEL_DIRECTORY = '../models/fine_tuned-opus-mt-en-ilo'
RANDOM_WORD_API_URL = ' https://random-word-form.herokuapp.com/random/noun?count=4'

translator = Translator(to_lang='ilo', model_path=EN_ILO_MODEL_DIRECTORY)

# Helper function to get word embeddings (replace with actual implementation)
def get_word_embeddings(word):
    return np.random.rand(50)  # Example: random embeddings of size 50

# Get random words with different difficulty levels
def get_random_words(difficulty):
    if difficulty == 'easy':
        RANDOM_WORD_API_URL = 'https://random-word-form.herokuapp.com/random/adjective?count=4'
    elif difficulty == 'medium':
        # TODO CHANGE PATH
        file_path = "services/en_normalized.txt"
        random_lines = get_random_lines(file_path, 4)
        print(random_lines)
        return random_lines
    elif difficulty == 'hard':
        RANDOM_WORD_API_URL = 'https://random-word-form.herokuapp.com/random/adjective?count=8'
    else:
        return None
    
    response = requests.get(RANDOM_WORD_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def translate_word(word):
    return translator.translate(word)

# TODO FIX THIS LOG
def calculate_score(selected_translation, is_correct):
    length = len(selected_translation)
    
    if is_correct=="true":
        return int(length)
    else:
        return -int(length)
    # if is_correct=="true":
    #     score = math.log(length + 1, 2) * 10
    # else:
    #     if length <= 5:
    #         score = -10 - (5 - length) * 5 
    #     else:
    #         score = -math.log(length, 2) * 5
            
    return int(score)



def get_random_lines(file_path, n):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            random_lines = random.sample(lines, n)
            return random_lines
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
