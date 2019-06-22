from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from os.path import join, dirname
from dotenv import load_dotenv

app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app.config.from_object(os.environ['APP_SETTINGS']) 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/getall")
def get_all():
    try:
        books=User.query.all()
        return jsonify([e.serialize() for e in books])
    except Exception as e:
	    return(str(e))
    
@app.route("/name/<name>")
def get_user_by_name(name):
    return "name : {}".format(name)

@app.route("/details")
def get_book_details():
    user=request.args.get('user') 
    return "User : {}".format(user)

if __name__ == '__main__':
    app.run()
