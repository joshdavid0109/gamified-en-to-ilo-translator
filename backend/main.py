from flask import Flask, request
from flask_cors import CORS
from receiver.routes import ai_blueprint


app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/user": {"origins": "http://127.0.0.1:5500"}})
# CORS(app, resources={r"/translate": {"origins": "http://127.0.0.1:5500"}})
# CORS(app, resources={r"/easy": {"origins": "http://127.0.0.1:5000"}})
# CORS(app, resources={r"/medium": {"origins": "http://127.0.0.1:5500"}})
# CORS(app, resources={r"/hard": {"origins": "http://127.0.0.1:5500"}})
# CORS(app, resources={r"/user": {"origins": "http://127.0.0.1:5500"}})
# CORS(app, resources={r"/submitanswer": {"origins": "http://127.0.0.1:5500"}})
# CORS(app, resources={r"": {"origins": "http://127.0.0.1:5500"}})

app.register_blueprint(ai_blueprint)
#app.logger.info(f"Received request: {request.json}")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
