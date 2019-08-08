#import all flask needed module
from flask import Flask,session,render_template,redirect,request,url_for,g
from flask import jsonify

import os

#import neural models and functions
from preprocess_data import user_data_process
from model import get_model,NN,NN1

import numpy as np
import pandas as pd

#import yaml file for database access configuration
import yaml

#app = Flask(__name__)
#'app' flask object
app = Flask(__name__, static_url_path='')

#create a secriate key to work with session
app.secret_key = os.urandom(24)

#database
from flask_mysqldb import MySQL
#from flaskext.mysql import MySQL

db = yaml.load(open('db.yaml'))

# DB connection configuration
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

#mysql object configure with app a=object
mysql = MySQL(app)

#keras model 
#model1 = get_model()
from keras.models import load_model

model = load_model("heart_attack_risk_prediction_percent_split.h5",compile= False)
model._make_predict_function()


def NN2(data):
    data = np.expand_dims(data, axis=0)
    #global model
    predections = model.predict_classes(data,verbose=0)
    probability = model.predict(data,verbose=0)
    print(probability[0][1])
    print(type(probability[0][1]))
    return predections[0],probability[0][1]


#function used before connectiong with server and user
@app.before_request
def before_request():
	g.user_email = None
	if 'user_email' in session:
		g.user_email = session['user_email']


#root directory
@app.route("/")
def index():
	#session['']
	if g.user_email:
		return render_template('index.html',login_flag = 1)	
	return render_template('index.html')

#signup durectory
@app.route("/signup", methods=['GET','POST']) # 
def signup():
	#cheick if the request is post method or get method
	if request.method == 'POST':
		#get form values
		email = request.form['email']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		password = request.form['password']

		#create cursor for database
		cur = mysql.connection.cursor()

		#check email
		qresult = cur.execute("""select email from member where email = %s""",(email,))
		#if email found return signup page
		if qresult > 0:
			mysql.connection.commit()
			cur.close()
			return render_template('signup.html',flag = 1)

		#if email not found insert user information to database
		cur.execute("INSERT INTO member(email,first_name,last_name,password) VALUES(%s,%s,%s,%s)",(email,first_name,last_name,password))

		#close database connection
		mysql.connection.commit()
		cur.close()
		#redirect to log in page
		return redirect(url_for('login',succ = 1))

	return render_template('signup.html')

#log in directory
@app.route("/login", methods=['GET','POST'])
def login():
	if request.method == 'POST':
		#get user values
		email = request.form['email']
		password = request.form['pass']

		#other varification section
		
		#create cursor for database
		cur = mysql.connection.cursor()
		# Database check if email and password match
		qresult = cur.execute("""select email from member where email = %s and password = %s""",(email,password))
		qfresult = cur.fetchone()
		#if not match then return login page with unsucccess
		if qresult <= 0:
			return render_template('login.html',flag = 1)
	
		#if email and password match then create session
		#pop existing session values if exist
		session.pop('user_email',None)
		#create session
		session['user_email'] = request.form['email']
		#return to mheart page
		return redirect(url_for('mheart'))
		#return render_template('mheart.html')

	#if log in then redirect to mheart page
	if g.user_email:
		return redirect(url_for('mheart'))
	return render_template('login.html')

#mheart directory
@app.route("/mheart") # 
def mheart():
	#check if log in
	if g.user_email:
		return render_template('predict.html',login_flag = 1)
	#if not log in then redirect to log in page
	return redirect(url_for('login'))


@app.route('/predict',methods=["POST"])
def predict():
	#get jeson values
	message = request.get_json(force=True)
	age = message['age']
	gender = message['gender']
	smoking = message['smoking']
	HTN = message['HTN']
	DPL = message['DPL']
	DM = message['DM']
	physical_exercise = message['physical_exercise']
	family_history = message['family_history']
	drug_history = message['drug_history']
	psychological_stress = message['psychological_stress']
	chest_pain = message['chest_pain']
	dyspnea = message['dyspnea']
	palpitation = message['palpitation']
	ECG = message['ECG']
	#process data
	data = user_data_process(message)
	
	x = []

	for key in data.keys():
		x.append(data[key])

	predicted_value,probability = NN2(x)
	print(probability)
	# Database insert new data
	cur = mysql.connection.cursor()
	cur.execute("INSERT INTO dataset(age,gender,smoking,HTN,DPL,DM,physical_exercise,family_history,drug_history,psychological_stress,chest_pain,dyspnea,palpitation,ECG,IHD,probability) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(age,gender,smoking,HTN,DPL,DM,physical_exercise,family_history,drug_history,psychological_stress,chest_pain,dyspnea,palpitation,ECG,predicted_value,probability))
	mysql.connection.commit()
	cur.close()

	result = ''
	if(predicted_value==1):
		result = 'According to the information our prediction result is YES'
	else:
		result = 'According to the information our prediction result is no'

	respone = {
	"gretting" : "hello,  Lets take a look at the information that you provide. your age is: "+age+". your gender is : "+gender+". your smoking habit: "+smoking+". HTN: "+HTN+". DPL: "+DPL+". DM: "+DM+". physical_exercise: "+physical_exercise+". your family_history: "+family_history+". drug_history: "+drug_history+". psychological_stress: "+psychological_stress+". chest_pain: "+chest_pain+". dyspnea: "+dyspnea+". palpitation: "+palpitation+". ECG Report: "+ECG+". ",
	"prediction" : result
	}

	return jsonify(respone)

#log out
@app.route("/logout")
def logout():
	#only of the user is log in
	if g.user_email:
		#delecte session value
		session.pop('user_email',None)
		return redirect(url_for('.index'))
	return redirect(url_for('.index'))


if __name__ == "__main__":
	app.run(host='0.0.0.0')
