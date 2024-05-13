from flask import Flask, request
from flask_cors import CORS
from receiver.routes import ai_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(ai_blueprint)
#app.logger.info(f"Received request: {request.json}")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
