from app.extensions import db

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique = True)
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    tasks = db.relationship('Tweets', back_populates='user')

    def serialize(self): 
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }