from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

Bootstrap(app)
ckeditor = CKEditor(app)
mail = Mail(app)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
