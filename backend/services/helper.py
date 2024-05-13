import firebase_admin, os, random

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

