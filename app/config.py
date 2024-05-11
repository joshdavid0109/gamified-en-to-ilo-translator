from flask import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
CORS(app, resources={r"/users": {"origins": "http://127.0.0.1:5500"}})

# Initialize Firebase
cred = credentials.Certificate(r'D:\flask_test\ai-database-a2089-firebase-adminsdk-bogd7-808afea2db.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ai-database-a2089-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Get a reference to the Firebase Realtime Database
ref = db.reference()

# You can include other configuration settings here
