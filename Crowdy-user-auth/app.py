from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import sys
from theater import theater
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'crowdy',
    'host': 'mongodb://schan2023:crowdyapp123@ds027748.mlab.com:27748/crowdy'
}

db = MongoEngine(app)
app.config['SECRET_KEY'] = 'CEN3031'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Homepage
@app.route('/')
def index():
	return render_template('/index.html')

class User(UserMixin, db.Document):
	meta = {'collection': 'users'}
	email = db.StringField(max_length=30)
	password = db.StringField()
	location = db.StringField()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

#FORMS
class RegForm(FlaskForm):
	email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=1, max=20)])
	location = StringField('Email',  validators=[InputRequired(), Length(max=30)])

class LogForm(FlaskForm):
	email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=1, max=20)])

#Register user
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                user = User(form.email.data,hashpass,form.location.data).save()
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)

#User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('dashboard'))
    form = LogForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

#User logout
@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#Retrieves all theaters by location and radius
@app.route('/dashboard', methods = ['POST', 'GET'])
@login_required
def dashboard():
	#Converts location string to longitude and latitude radiusString
	geocodeUrl = "https://maps.googleapis.com/maps/api/geocode/json"
	paramsGeocode = dict(
		address=current_user.location,
		key='AIzaSyBBABVNXk90RVdvQqgDanDifw-bgMGeONI'
	)
	resp = requests.get(url=geocodeUrl, params=paramsGeocode).content
	respParse = json.loads(resp)
	lng = str(respParse["results"][0]["geometry"]["location"]["lng"])
	lat = str(respParse["results"][0]["geometry"]["location"]["lat"])

	#Finds movie theaters based on longitude and latitude and radius
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
	params = dict(
		location=lat + ',' + lng,
		radius=40000,
		type='movie_theater',
		key='AIzaSyBBABVNXk90RVdvQqgDanDifw-bgMGeONI'
	)
	data = requests.get(url=url, params=params).content
	parseData = json.loads(data)
	list = []

	for item in parseData["results"]:
		tempT = theater()
		tempT.name = item["name"]
		tempT.address = item["vicinity"]
		#tempT.rating = item["rating"]
		list.append(tempT)

	return render_template('display_theaters.html', list=list)

if __name__ == '__main__':
	app.run(debug = True)
