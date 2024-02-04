from flask import Flask
from flask_cors import CORS
# ... other necessary imports ...
from .config import DevelopmentConfig

from .routes import api_bp  # Import the Blueprint
from .user_routes import user_bp  # Import the Blueprint

from flask_migrate import Migrate
from models import db

app = Flask(__name__)
CORS(app, support_credentials=True)

# ... other app configurations ...
app.config.from_object(DevelopmentConfig)  # Load development config
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(api_bp)  # Register the Blueprint with the app
app.register_blueprint(user_bp)  # Register the Blueprint with the app

with app.app_context():
    db.drop_all()  # This will drop all tables
    db.create_all()  # This will recreate tables based on the models

# ... rest of your app code ...
