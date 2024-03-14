from flask_mongoengine import MongoEngine
from mongoengine.fields import DateTimeField
from datetime import datetime
from models.auth import Auth  

db = MongoEngine()

class User(db.Document):
    auth_id = db.ReferenceField(Auth)
    username=db.StringField(required=False)
    firstName = db.StringField(required=True)
    lastName = db.StringField(required=False)  
    gender = db.StringField(required=False)
    phone_number = db.StringField(required=False)
    cnic_number = db.StringField(required=True)
    organization = db.StringField(required=True)
    ntn_number = db.StringField(default='0')
    country = db.StringField(required=True)
    province = db.StringField(required=True)
    city = db.StringField(required=True)
    address = db.StringField(required=True)
    subscription = db.StringField(choices=["common", "premium", "super"], default="common")
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def to_json(self):
        return {
            "auth_id": str(self.auth_id),
            "firstName": self.firstName,
            "lastName": self.lastName,
            "gender": self.gender,
            "phone_number": self.phone_number,
            "cnic_number": self.cnic_number,
            "organization": self.organization,
            "ntn_number": self.ntn_number,
            "country": self.country,
            "province": self.province,
            "city": self.city,
            "address": self.address,
            "subscription": self.subscription,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
