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

# Use the access token to make an authenticated API requesta
url = 'https://translation.googleapis.com/v3/projects/caramel-galaxy-423217-u2/locations/global:translateText'
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
data = {
    'contents': ['how many is the onion?'],
    'targetLanguageCode': 'ilo'
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print('Success:', response.json())
else:
    print('Error:', response.status_code, response.text)
