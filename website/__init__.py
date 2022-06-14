from os import path
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)



admin = Admin(app,template_mode='bootstrap3')

from website import views, models

if not path.exists('website/' + DB_NAME):
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = '/'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))

