from flask import Flask, request
from flask_cors import CORS
from receiver.routes import ai_blueprint


app = Flask(__name__, template_folder="receiver/templates", static_folder="receiver/templates/assets")
app.secret_key = "gamified-translator"
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}}) 


app.register_blueprint(ai_blueprint)
#app.logger.info(f"Received request: {request.json}")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
