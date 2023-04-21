from . import db
from . import Migrate
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    full_name = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.DateTime, default=datetime.datetime.now())
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    contact = db.relationship("Contact", backref="user", lazy="dynamic", cascade="all,delete")

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        last_seen = db.Column(db.DateTime(), default=datetime.datetime.utcnow)




class Contact(db.Model,UserMixin):
    __tablename__ = "contact"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256))
    state = db.Column(db.String(256))
    city = db.Column(db.String(256))
    country = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))


