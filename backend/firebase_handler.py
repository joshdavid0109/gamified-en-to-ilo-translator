
import firebase_admin, os, requests, random
from firebase_admin import credentials, db
import json

# Initialize Firebase
# cred = credentials.Certificate('../../flask_test/ai-database-a2089-firebase-adminsdk-bogd7-808afea2db.json')
cred = credentials.Certificate('ai-database-a2089-firebase-adminsdk-bogd7-808afea2db.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ai-database-a2089-default-rtdb.asia-southeast1.firebasedatabase.app/'
})


def authenticate_user(username, password):
    try:
        ref = db.reference('users')

        # Check if the username exists in the database
        user_ref = ref.order_by_child('username').equal_to(username).get()

        if not user_ref:
            return json.dumps({"success": False, "error": "User not found"})
    
        user_id = list(user_ref.keys())[0]
        user_data = user_ref[user_id]
        if user_data['password'] == password:
            return json.dumps({"success": True, "user_id": user_id, "username": user_data['username'] , "points": user_data['points'], "tier": user_data['tier'] })
        else:
            return json.dumps({"success": False, "error": "Incorrect password"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

#test

print(authenticate_user('kiko123', 'kiko123'))


# Get a reference to the user's data
ref = db.reference('/users/user0001')

# Mapping of points to tiers
points_tiers = {
    (0, 50): 'Beginner',
    (51, 100): 'Apprentice',
    (101, 250): 'Intermediate',
    (251, 500): 'Explorer',
    (501, 1000): 'Linguist',
    (1001, 1500): 'Scholar',
    (1501, 2000): 'Proficient',
    (2001, 3000): 'Master',
    (3001, 5000): 'Maestro',
    (5001, 7500): 'Maestro +',
    (7501, 10000): 'Virtuoso'
}

def update_points(user_id, points):
    try:
        # Get a reference to the user's data
        user_ref = db.reference(f'/users/{user_id}')
        user_data = user_ref.get()

        if not user_data:
            return json.dumps({"success": False, "error": "User not found"})

        # Update the points and tier
        user_data = update_tier(user_data, points)

        # Save the updated data back to the database
        user_ref.update(user_data)

        return json.dumps({"success": True, "user_id": user_id, "username": user_data['username'], "points": user_data['points'], "tier": user_data['tier']})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
        
# Function to update tier based on points
def update_tier(current_data, points):
    if current_data is None:
        current_data = {'points': 0, 'tier': 'Beginner'}  # Set initial values if none exist

    # Update points
    current_data['points'] += points

    # Update tier
    for range_points, tier in points_tiers.items():
        if range_points[0] <= current_data['points'] <= range_points[1]:
            current_data['tier'] = tier
            break

    return current_data

# Example usage (galing sa user data)
# current_data = {'points': 20, 'tier': 'Beginner'}
# current_data = update_tier(current_data, 3)
# print(current_data)

def get_leaderboard():
    # Get a reference to the users node
    users_ref = db.reference('/users')

    # Fetch and sort users, handling integers
    sorted_users = sorted(
        users_ref.get().items(),
        key=lambda item: (
            item[1] if isinstance(item[1], int) else item[1].get('points', 0), 
            item[1].get('username', 'Unknown') if isinstance(item[1], dict) else 'Unknown'  # Handle username too
        ),
        reverse=True
    )[:5]

    # Print leaderboard
    for _, user_data in sorted_users:
        points = user_data if isinstance(user_data, int) else user_data.get('points', 0)
        username = user_data.get('username', 'Unknown') if isinstance(user_data, dict) else 'Unknown'
        print(f"User: {username}, Points: {points}")