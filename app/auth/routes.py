from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity

from app.extensions import db, jwt
from app.auth import authBp
from app.models.user import Users
from app.models.blacklist_token import BlacklistToken

@authBp.route("/register", methods=['POST'], strict_slashes =False)
def registration():
    # get data from request json
    data = request.get_json()
    
    # get username password email from json
    username = data.get('username', None)
    password = generate_password_hash(data.get('password', None))
    email = data.get('email', None)
    
    error = None

    # validasi input
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    
    if error is None:
        try:
            db.session.add(Users(username=username,
                                password=password,
                                email=email))
            db.session.commit()
        except db.IntegrityError:
            error = f"User {username} is already registered."
        
            return jsonify({
                "message": "Registration user is completed",}), 200
        
    # jika terdapat error tampilkan dengan flask
    if error:
        return jsonify({"error": error})

    # jika berhasil berikan message berhasil login
    return jsonify({"message":"Berhasil Registrasi",}), 200

@authBp.route("/login", methods=['POST'], strict_slashes = False)
def login():
    # get data from request json
    data = request.get_json()
    
    # get username password from json
    username = data.get('username', None)
    password = data.get('password', None)

    # validasi input
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    
    error = None
    # query record user dari database dengan username request
    user = db.session.execute(db.select(Users).filter_by(username=username)).scalar_one()

    # cek apakah user ada
    if user is None:
        error = "username not found"
    elif not check_password_hash(user.password, password):
        error = "Incorrect password"
    # ditambahkan
    else:
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id)
    
    # jika terdapat error tampilkan dengan flask
    if error:
        return jsonify({"error": error}), 422

    # jika berhasil berikan message berhasil login
    return jsonify({
        "message":"Berhasil Login",
        "access_token" : access_token,
        "refresh_token" : refresh_token}), 200

@authBp.route('/refresh', methods=['POST'])
@jwt_required(refresh = True)
def refresh():
    current_user = get_jwt_identity()
    access_token = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(access_token), 200

@authBp.route("/logout", methods=['POST'], strict_slashes = False)
@jwt_required(locations=["headers"])
def logout():
    # mendapatkan token jwt
    raw_jwt = get_jwt()
    print(raw_jwt)

    # menambahkan token jwt ke blacklist
    # mencabut JWT dan menolak akses ke permintaan di masa mendatang
    jti = raw_jwt.get('jti')
    token = BlacklistToken(jti = jti)
    
    db.session.add(token)
    db.session.commit()
    return jsonify(message = "logout successfully")

# callback untuk memeriksa apakah JWT ada di daftar blokir atau tidak
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = BlacklistToken.query.filter_by(jti=jti).first()
    return token_in_redis is not None