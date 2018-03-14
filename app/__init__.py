from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# create app instance and set up config
app = Flask(__name__)
app.config.from_object(Config)

# create database and migration functionality
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models
