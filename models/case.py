from flask_mongoengine import MongoEngine
from mongoengine import StringField, ListField, EmbeddedDocument, EmbeddedDocumentField, MapField, ReferenceField
from datetime import datetime
from mongoengine.fields import DateTimeField
from models.users import User  
db = MongoEngine()

class Dates(EmbeddedDocument):
    DateOfHearing = StringField()
    JudgmentDate = StringField()
    NotificationDate = StringField()

class Case(db.Document):
    user_id = db.ReferenceField(User)
    # user_id = ReferenceField('User', required=True)  # Add reference to User
    JudgeNames = ListField(StringField())
    People = ListField(StringField())
    Organizations = ListField(StringField())
    Locations = ListField(StringField())
    Dates = EmbeddedDocumentField(Dates)
    CaseNumbers = ListField(StringField())
    Appellants = ListField(StringField())
    Respondents = ListField(StringField())
    Money = ListField(StringField())
    FIRNumbers = ListField(StringField())
    ReferenceArticles = ListField(StringField())
    ReferredCases = ListField(StringField())
    ReferredCourts = ListField(StringField())
    AppealCaseNumbers = ListField(StringField())
    AppealCourtNames = ListField(StringField())
    CaseApproval = StringField()
    ExtractiveSummary = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def to_json(self):
        # Ensure you handle the serialization of the user reference correctly
        user_id = str(self.user_id) if self.user_id else None
        dates = {
            "DateOfHearing": self.Dates.DateOfHearing,
            "JudgmentDate": self.Dates.JudgmentDate,
            "NotificationDate": self.Dates.NotificationDate,
        }

        return {
            "user": user_id,
            "JudgeNames": self.JudgeNames,
            "People": self.People,
            "Organizations": self.Organizations,
            "Locations": self.Locations,
            "Dates": dates,
            "CaseNumbers": self.CaseNumbers,
            "Appellants": self.Appellants,
            "Respondents": self.Respondents,
            "Money": self.Money,
            "FIRNumbers": self.FIRNumbers,
            "ReferenceArticles": self.ReferenceArticles,
            "ReferredCases": self.ReferredCases,
            "ReferredCourts": self.ReferredCourts,
            "AppealCaseNumbers": self.AppealCaseNumbers,
            "AppealCourtNames": self.AppealCourtNames,
            "CaseApproval": self.CaseApproval,
            "ExtractiveSummary": self.ExtractiveSummary,
            "created_at": self.created_at, 
            "updated_at": self.updated_at
        }

