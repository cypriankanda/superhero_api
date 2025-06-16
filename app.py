# app.py
from flask import Flask
from flask_migrate import Migrate
from models import db  # ✅ import the db instance
import models  # ✅ import models to register them

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///superheroes.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    return app
