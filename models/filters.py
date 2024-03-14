from mongoengine import Document, ListField, StringField
from mongoengine.fields import DateTimeField
from flask_mongoengine import MongoEngine
from datetime import datetime
db = MongoEngine()

class Filters(db.Document):
    JudgeFilters = db.ListField(db.StringField(), default=list)
    CaseTypeFilters = db.ListField(db.StringField(), default=list)
    LocationFilters = db.ListField(db.StringField(), default=list)
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)

    def to_json(self):
        return {
            "JudgeFilters": self.JudgeFilters,
            "CaseTypeFilters": self.CaseTypeFilters,
            "LocationFilters": self.LocationFilters,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
