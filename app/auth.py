from flask_httpauth import HTTPBasicAuth
from . import db
from .models import User

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify(username, password):
    user = db.session.execute(db.select(User).where(User.username==username)).scalar_one_or_none()
    if user is not None and user.checkpw(password):
        return user
    return None


@basic_auth.error_handler
def handle_error(status_code):
    return {'error': 'Incorrect username and/or password. Try again'}, 401