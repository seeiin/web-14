from flask import Blueprint

tweetBp = Blueprint('tweet', __name__)

from app.tweet import routes