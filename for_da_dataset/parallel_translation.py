from google.oauth2 import service_account
import google.auth.transport.requests
import requests

# Correct file path using raw string
service_account_file = r'D:\flask_test\caramel-galaxy-423217-u2-4a1eac827db8.json'

# Load the service account key JSON file
credentials = service_account.Credentials.from_service_account_file(
    service_account_file,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Request an access token
request = google.auth.transport.requests.Request()
credentials.refresh(request)
access_token = credentials.token

def translate_to_ilocano(text):
    url = 'https://translation.googleapis.com/v3/projects/caramel-galaxy-423217-u2/locations/global:translateText'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'contents': [text],
        'targetLanguageCode': 'ilo'
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['translations'][0]['translatedText']
    else:
        print('Error:', response.status_code, response.text)
        return None  # Handle errors gracefully

# Read English phrases from file
english_file = 'scraped_phrases.txt'  # Update the path
with open(english_file, 'r', encoding='utf-8') as file:
    english_phrases = file.readlines()

# Store translations
ilocano_phrases = []
for phrase in english_phrases:
    ilocano_translation = translate_to_ilocano(phrase.strip())  # Remove newlines
    if ilocano_translation:  # Only append if translation was successful
        ilocano_phrases.append(ilocano_translation)

# Create a dictionary for parallel storage (optional)
translations = dict(zip(english_phrases, ilocano_phrases))

# Output results (choose one)
# 1. Print to console
for eng, ilo in zip(english_phrases, ilocano_phrases):
    print(f"English: {eng.strip()}\nIlocano: {ilo}\n")

# 2. Save to a new file (optional)
ilocano_file = 'ilocano_phrases.txt'  # Update the path
with open(ilocano_file, 'w', encoding='utf-8') as file:
    for phrase in ilocano_phrases:
        file.write(phrase + '\n')

# ... (you can further process translations as needed) ...
