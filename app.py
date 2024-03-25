from flask import Flask # Import the Flask class from the flask module


# Create an instance of Flask called app which will be the central object
app = Flask(__name__)


# define a route
@app.route('/')
def index():
    firstname = 'Garren'
    age = 123
    return 'Hello ' + firstname + ' ' + str(age) + ' years old'
