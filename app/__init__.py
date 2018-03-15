from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flaskext.markdown import Markdown
from flask_bootstrap import Bootstrap

# create app instance and set up config
app = Flask(__name__)
app.config.from_object(Config)

# create database and migration functionality
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# create login functionality and login_required pages
login = LoginManager(app)
login.login_view = "login"

# create markdown functionality
markdown = Markdown(app)

# create bootstrap functionality (for quick_form)
bootstrap = Bootstrap(app)

from app import routes, models
