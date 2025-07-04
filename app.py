from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db
from routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprint
    app.register_blueprint(api)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
