from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__setpassword(kwargs.get('password', ''))

    def __repr__(self):
        return f'<User {self.id}|{self.username}>'

    def __setpassword(self, plaintextpw):
        self.password = generate_password_hash(plaintextpw)
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def checkpw(self, plaintextpw):
        return check_password_hash(self.password, plaintextpw)
