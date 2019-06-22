from flask import Flask, request, jsonify, render_template
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
        users=User.query.all()
        return jsonify([u.serialize() for u in users])
    except Exception as e:
	    return(str(e))

@app.route("/add/form",methods=['GET', 'POST'])
def add_user_form():
    if request.method == 'POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        try:
            user=User(
                username=username,
                email=email,
                password=User.generate_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            return "User added. user id={}".format(user.id)
        except Exception as e:
            return(str(e))
    return render_template("create_user.html")

@app.route("/login",methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')

        try:
            user=User.query.filter_by(email=email).first()
            if User.verify_hash(password, user.password):
                return render_template("create_user.html", msg='success')
            else: 
                return render_template("login.html", msg='wrog credentials') 
        except Exception as e:
            return render_template("login.html", msg='wrog credentials')
    return render_template("login.html")

if __name__ == '__main__':
    app.run()
