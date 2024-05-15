from flask import jsonify
from .config import app, ref
from flask_cors import CORS


@app.route('/')
def index():
    return "test index"

@app.route('/users', methods=['POST'])
def get_users():
    users = ref.child('users').get()
    return jsonify(users)
