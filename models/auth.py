from flask_mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()

class Auth(db.Document):
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)

    def to_json(self):
        return {"email": self.email,  "role": self.role, "created_at": self.created_at, "updated_at": self.updated_at}

