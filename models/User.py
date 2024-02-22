from models import db  # Import db from the models module


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))  # New field for name
    email = db.Column(db.String(100))  # New field for email
    age = db.Column(db.Integer)  # New field for age
    subscription_plan = db.Column(db.String(50))  # New field for subscription plan
    color = db.Column(db.String(100))
    preferred_language = db.Column(db.String(100))
    conversation_history = db.Column(db.String(100))

