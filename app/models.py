import secrets
from . import db
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    posts = db.relationship("Post", back_populates='author')
    token = db.Column(db.String, index=True, unique=True)
    token_expiration = db.Column(db.DateTime(timezone=True))
    comments = db.relationship('Comment', backref='user')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setpassword(kwargs.get('password', ''))

    def __repr__(self):
        return f'<User {self.id}|{self.username}>'

    def setpassword(self, plaintextpw):
        self.password = generate_password_hash(plaintextpw)
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def checkpw(self, plaintextpw):
        return check_password_hash(self.password, plaintextpw)

    def to_dict(self):
        return {'id': self.id,
    'firstName': self.first_name,
    'lastName': self.last_name,
    'username': self.username,
    'dateCreated': self.date_created
}
    
    def get_token(self):
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return {"token": self.token, "tokenExpiration": self.token_expiration}
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(hours=1)
        self.save()
        return {"token": self.token, "tokenExpiration": self.token_expiration}

            


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    


    # in sql - user id INTEGER NOT NULL, foreign key (user_id) references user(id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', backref='post')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save()
    
    def __repr__(self):
        return f'<Post {self.id}|{self.title}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "dateCreated": self.date_created,
            "author": self.author.to_dict(),
            "comments": [comment.to_dict() for comment in self.comments]
        }
    
    def update(self, **kwargs):
        allowed_fields = {'title', 'body'}

        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(self, key, value)
        self.save()

    def delete(self):
        db.session.delete(self) # deleting THIS obj from the db
        db.session.commit() # commiting our changes


# create comments class/table
class Comment(db.Model):
    # create table
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    # user = db.relationship('User', back_populates='comments')

    # insert into
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save()

    def __repr__(self):
        return f'<Comment {self.id}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'dateCreated': self.date_created,
            'user': self.user.to_dict()
        }