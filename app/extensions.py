from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager # ditambah

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()