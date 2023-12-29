# app.py
from flask import Flask
import secrets


app = Flask(__name__, template_folder='templates')
app.secret_key = secrets.token_hex(16)  # Replace with a secure secret key

if __name__ == "__main__":
    from src.routes import main_blueprint

    app.register_blueprint(main_blueprint)
    app.run(host='0.0.0.0', port=5000, debug=True)