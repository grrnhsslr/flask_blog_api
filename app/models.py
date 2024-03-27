from . import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

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

    def to_dict(self):
        return {'id': self.id,
    'firstname': self.first_name,
    'lastName': self.last_name,
    'username': self.username,
    'dateCreated': self.date_created
}
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    # in sql - user id INTEGER NOT NULL, foreign key (user_id) references user(id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save()
    
    def __repr__(self):
        return f'<Post {self.id}|{self.title}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
