# app.py
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Replace with a secure secret key

if __name__ == "__main__":
    from routes import main_blueprint

    app.register_blueprint(main_blueprint)
    app.run(debug=True)
