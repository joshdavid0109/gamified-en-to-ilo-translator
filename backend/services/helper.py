import firebase_admin, os, random, requests
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import random

en_ilo_tokenizer = None
en_ilo_model = None

def load_model_and_tokenizer(model_name):
    global en_ilo_tokenizer, en_ilo_model
    if en_ilo_tokenizer is None or en_ilo_model is None:
        en_ilo_tokenizer = AutoTokenizer.from_pretrained(model_name)
        en_ilo_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        print("SHOULD RUN ONLY ONCE")
        print("load_model_and_tokenizer")
    return en_ilo_tokenizer, en_ilo_model

def translate_text(tokenizer, model, text):
    input_ids = tokenizer(text, return_tensors="pt")["input_ids"]
    generated_sequence = model.generate(input_ids=input_ids)[0].numpy().tolist()
    translated_text = tokenizer.decode(generated_sequence, skip_special_tokens=True)
    return translated_text

#load models and tokenizers
models_dir = os.path.join('..', 'models', 'fine_tuned-opus-mt-en-ilo')
# ilo_en_tokenizer, ilo_en_model = load_model_and_tokenizer("../models/opus-mt-ilo-en/")
en_ilo_tokenizer, en_ilo_model = load_model_and_tokenizer("C:/Users/franz/vscode/gam/gamified-en-to-ilo-translator/backend/models/fine_tuned-opus-mt-en-ilo")
# en_ilo_tokenizer, en_ilo_model = load_model_and_tokenizer(models_dir)

EN_ILO_MODEL_DIRECTORY = '../models/opus-mt-ilo-en'
ILO_EN_MODEL_DIRECTORY = '../models/opus-mt-en-ilo'
FINE_ILO_EN_MODEL_DIRECTORY = '../models/fine_tuned-opus-mt-en-ilo'
RANDOM_WORD_API_URL = ' https://random-word-form.herokuapp.com/random/noun?count=4'

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

#target ilo
def translate_word(word):
    return translate_text(en_ilo_tokenizer, en_ilo_model, word)

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

