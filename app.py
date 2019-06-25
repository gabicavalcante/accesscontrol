import os
from os.path import join, dirname

from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)
login = LoginManager(app)

from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from utils import read_config_file
import orion
import json 

config = read_config_file('config.ini')
with open(config.get('device_schema_path')) as json_file:
    data = json.load(json_file)
orion.init(config.get('orion_host'), config.get('orion_port'))

from models import User, Device

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(401)
def unauthorized_access(e):
    # note that we set the 404 status explicitly
    return render_template('401.html'), 401

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/getall/users")
@login_required
def get_all_users():
    try:
        users = User.query.all()
        return jsonify([u.serialize() for u in users])
    except Exception as e:
        return(str(e))

@app.route("/getall/devices")
@login_required
def get_all_devices():
    try:
        devices_db = Device.query.order_by(Device.device_id.asc()).all()
        devices = []
        for device in devices_db: 
            device_id = device.device_id 
            #entity = orion.get_entities_by_id(device_id)
            if entity: 
                info = { 
                    'device_id': entity.get('id'),
                    'device_type': entity.get('type'),
                    'description': device.description,
                    'status': True if entity.get('status').get('value') == 'true' else False,
                }
                devices.append(info)
        return render_template('devices_list.html', devices=devices)
    except Exception as e:
        return(str(e))

#@login_required
@app.route("/add/user", methods=['GET', 'POST'])
def add_user_form():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = User(
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

@app.route("/add/device", methods=['GET', 'POST'])
@login_required
def add_device_form():
    if request.method == 'POST':
        device_id = request.form.get('device_id')
        device_type = request.form.get('device_type')
        description = request.form.get('description')
        status = bool(request.form.get('status')) 

        ## ORION
        #orion.register_entity(data, device_type, device_id, '0.0.0.0:4000')
        try:
            device = Device(
                device_id=device_id,
                device_type=device_type,
                description=description,
                status=status
            )
            db.session.add(device)
            db.session.commit()
            return render_template("create_device.html")
        except Exception as e:
            return(str(e))
    return render_template("create_device.html")

@app.route("/doorcontrol", methods=['POST'])
@login_required
def doorcontrol():  
    status = request.form.get('status')
    device_status = True if status == 'true' else False
    device_id = request.form.get('device_id') 
    
    device = Device.query.filter_by(device_id=device_id).first()
    if device:
        device.status = device_status
        db.session.commit()
        #orion.update_context(device.device_id, device.device_type, status)
    return "sucess"
    


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('get_all_devices'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
 
        try:
            user = User.query.filter_by(email=email).first() 
            if User.verify_hash(password, user.password):
                login_user(user, remember=True)
                return redirect(url_for('get_all_devices'))
            else:
                flash('Invalid username or password')
                return redirect(url_for('login'))
        except Exception as e:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
