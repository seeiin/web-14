from app.extensions import db

class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship('Users', back_populates = 'tasks')

    def serialize(self): 
        return {
            "id": self.id,
            "content": self.content,
            "user_id" : self.user_id
        }
    
