from flask import request, jsonify
from app.extensions import db

from app.tweet import tweetBp
from app.models.tweet import Tweets

from flask_jwt_extended import jwt_required, get_jwt_identity


@tweetBp.route("", methods=['GET'], strict_slashes = False)
@jwt_required(locations=["headers"], optional=True)
def get_tweet():
    limit = request.args.get('limit', 10)
    if type(limit) is not int:
        return jsonify({'message': 'invalid parameter'}), 400
    
    user_id = get_jwt_identity()

    if not user_id:
        user_id = "None"
    else:
        user_id = user_id

    tweets = db.session.execute(
        db.select(Tweets).limit(limit)
    ).scalars()

    result = []
    for tweet in tweets:
        result.append(tweet.serialize())

    return jsonify(
        user_id = user_id,
        data=result
    ), 200


@tweetBp.route("", methods=['POST'], strict_slashes = False)
@jwt_required(locations=["headers"])
def post_tweet():
    data = request.get_json()
    content = data.get('content', None)

    if not content:
        return jsonify({'error': 'Invalid data'}), 422
    
    user_id = get_jwt_identity()

    tweet = Tweets(
        user_id = user_id,
        content=content
    )
    db.session.add(tweet)
    db.session.commit()
    return jsonify(data=tweet.serialize()), 200