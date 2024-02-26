from models import db  # Import db from the models module

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    length = db.Column(db.Integer, nullable=False)  # Duration in minutes
    date = db.Column(db.Date, nullable=False)
    agent_name = db.Column(db.String(100), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    agent_email = db.Column(db.String(100), nullable=False)  # New field for agent's email
    customer_email = db.Column(db.String(100), nullable=False)  # New field for customer's email
    user_id = db.Column(db.Integer, nullable=False)  # Foreign key to User model

# Assuming the User model is as provided
