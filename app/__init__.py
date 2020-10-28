from flask import Flask

from config import Config

# Import for Flask DB and Migrator
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create instance of Flask class, name it app
app = Flask(__name__)
# Add configurations
app.config.from_object(Config)

# Create db and migrator
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
