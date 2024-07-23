import os
from flask import Flask, send_from_directory
from flask_login import LoginManager
from dotenv import load_dotenv
from src.models import db, Users
from src.api import api

# load .env file
load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DEBUG = os.getenv("DEBUG")
SECRET = os.getenv("SECRET_KEY")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


if not all([HOST, PORT, DEBUG]):
    raise ValueError("HOST, PORT or DEBUG must be set")

if not SECRET:
    raise ValueError("SECRET must be set")

if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB]):
    raise ValueError("POSTGRES_USER, POSTGRES_PASSWORD or POSTGRES_DB must be set")

DB_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:5432/{POSTGRES_DB}"

# Init and config
app = Flask(__name__)

# Register blueprints
app.register_blueprint(api, url_prefix="/api")

app.static_folder = "./frontend/dist"
app.static_url_path = ""
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SECRET_KEY"] = SECRET

# init db
db.init_app(app)

# init login manager
login_manager = LoginManager()
login_manager.init_app(app)

# create tables
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first() or None


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path=""):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")




if __name__ == "__main__":
    DEBUG = True if DEBUG.lower() == "true" else False
    app.run(debug=DEBUG, host=HOST, port=PORT)
