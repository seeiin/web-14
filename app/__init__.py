from flask import Flask
from config import Config
from app.extensions import db, migrate, jwt

from app.tweet import tweetBp
from app.user import userBp
from app.auth import authBp

def create_app(config_class=Config):
    # Konfigurasi APP
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initilizae database & migration
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # initilize blueprint
    app.register_blueprint(tweetBp, url_prefix='/tweets')
    app.register_blueprint(userBp, url_prefix='/users')
    app.register_blueprint(authBp, url_prefix='/auth')

    return app