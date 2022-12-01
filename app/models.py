from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True)
    name = db.Column(db.String(100), index=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return '<User %r>' % self.name

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    used_technology = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    img_fg_path = db.Column(db.String(250), nullable=False)
    img_bg_path = db.Column(db.String(250), nullable=False)
    github_url = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<Project %r>' % self.name
