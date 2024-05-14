
import firebase_admin, os, requests, random
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate('../gamified-en-to-ilo-translator/ai-database-a2089-firebase-adminsdk-bogd7-808afea2db.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ai-database-a2089-default-rtdb.asia-southeast1.firebasedatabase.app/'
})


def authenticate_user(username, password):
    try:
        ref = db.reference('users')

        # Check if the username exists in the database
        user_ref = ref.order_by_child('username').equal_to(username).get()

        if not user_ref:
            return False, "User not found"
    
        user_id = list(user_ref.keys())[0]
        user_data = user_ref[user_id]
        if user_data['password'] == password:
            return True, user_id
        else:
            return False, "Incorrect password"
    except Exception as e:
        return False, str(e)

#test

print(authenticate_user('kiko123', 'kiko123'))