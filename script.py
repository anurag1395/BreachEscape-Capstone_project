import os
import numpy as np
import sklearn.ensemble.forest
import flask
import pickle
from flask import Flask, render_template, request
from flask_mail import Mail
from dbconnect import connection
from flask_mail import Message
#creating instance of the class
app=Flask('__name__')
app.config.update(dict(
        DEBUG = True,
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_USERNAME = 'breachescape.helpdesk@gmail.com',
        MAIL_PASSWORD = 'BreachEscape@09'))
mail = Mail(app=app)
is_logged_in = "Log In"
#to tell flask what url shoud trigger the function inde
# x()
@app.route('/')
@app.route('/home',methods = ['POST','GET'])
def home():
    return flask.render_template('home.html',is_logged_in=is_logged_in)

#prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,19)
    loaded_model = pickle.load(open("Final_model.pkl","rb"))
    result = loaded_model.predict_proba(to_predict)
    return result[0]

@app.route('/signup',methods = ['POST','GET'])
def signup():
    return flask.render_template('signup.html',is_logged_in=is_logged_in)


@app.route('/loggedin',methods = ['POST','GET'])
def loggedin():
    global is_logged_in
    if request.method == 'POST':
        contact_info = request.form.to_dict()
        contact_info=list(contact_info.values())
    c,conn = connection()
    sql = "Select * from Login_details where Email=%s and Passwd=%s"
    row_count = c.execute(sql, (contact_info[0],contact_info[1]))
    conn.commit()
    print (contact_info[0])
    print (row_count)
    if row_count==0:
        print ("Username not Found")
        return flask.render_template('loginfailure.html',is_logged_in=is_logged_in)
    else:
        print ("Username found")
        is_logged_in = "Log Out"
        return flask.render_template('loginsuccess.html',is_logged_in=is_logged_in)
    #return flask.render_template('test.html',is_logged_in=is_logged_in)

@app.route('/navlogin',methods = ['POST','GET'])
def navlogin():
    global is_logged_in
    if is_logged_in == "Log In":
        print (is_logged_in)
        return flask.render_template('login_request.html',is_logged_in="Log In")
    else :
        is_logged_in ="Log In"
        return flask.render_template('logout.html',is_logged_in="Log In")

@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)
        result =result[1]
        risk_score = round(result,2)
        if (round(result,2)>=0 and (round(result,2)<=0.3)):
            prediction=' Your Risk Level : Minimal'
            desc1='1. A breach with no material effect.'
            desc2='2. Usually less than one thousand records.'
            desc3='3. Breach notification required, but little damage done.'
        elif (round(result,2)>0.3) and (round(result,2)<=0.5):
            prediction='Your Risk Level : Moderate'
            desc1='A breach with low long-term business impact.' 
            desc2='Usually involves the loss of several thousands of records of semi sensitive information.'
            desc3='Limited breach notification and financial exposure.'
        elif (round(result,2)>0.5) and (round(result,2)<=0.65) :
            prediction='Your Risk Level : High'
            desc1='A breach with likely short to midterm exposure to business.'
            desc2='Legal and/or regulatory impact.'
            desc3='Usually tens of thousands of records of moderate sensitive information involved.'
            desc4='Some breach notification and financial loss.'
        elif (round(result,2)>0.65) and (round(result,2)<=0.85) :
            prediction='Your Risk Level : Critical'
            desc1='A breach with significant exposure to business, legal and or regulatory impact.'
            desc2='Large amount of sensitive information lost (usually hundreds of thousands to millions of records).'
            desc3='Significant notification process costs involved and public image impact.'
        elif (round(result,2)>0.85) and (round(result,2)<=1) :
            prediction='Your Risk Level : Catastrophic'
            desc1='Breach with immense long term impact on breached organization, customers and/or partners.'
            desc2='Very large amount of highly sensitive information lost (usually 10-100+ million records).'
            desc3='Massive notification process.'
            desc4='Potentially existential financial loss for breached organization in remediation and related costs.'
            desc5='Use of lost sensitive information seen.'

    return render_template("result.html",prediction=prediction,desc1=desc1,desc2=desc2,desc3=desc3,risk_score=risk_score)

@app.route('/test',methods = ['POST','GET'])
def test():
    if is_logged_in == "Log In":
        print (is_logged_in)
        #Login()
        return flask.render_template('login_request.html',is_logged_in=is_logged_in)
    else :
        return flask.render_template('test.html',is_logged_in=is_logged_in)


@app.route('/contactus',methods = ['POST','GET'])
def contactus():
    return flask.render_template('contactus.html',is_logged_in=is_logged_in)

@app.route('/dashboard',methods = ['POST','GET'])
def dashboard():
    return flask.render_template('dashboard.html',is_logged_in=is_logged_in)

@app.route('/thankyou',methods = ['POST','GET'])
def thankyou():
    if request.method == 'POST':
        contact_info = request.form.to_dict()
        contact_info=list(contact_info.values())
    c,conn = connection()
    sql = "INSERT INTO Contact_us VALUES (%s, %s,%s,%s,%s)"
    c.execute(sql, (contact_info[0],contact_info[1],contact_info[2],contact_info[3],contact_info[4]))
    conn.commit()
    return flask.render_template('thankyou.html',is_logged_in=is_logged_in)

@app.route('/successful_registration',methods = ['POST','GET'])
def successful_registration():
    if request.method == 'POST':
        login_info = request.form.to_dict()
        login_info=list(login_info.values())
    print(login_info)
    c,conn = connection()
    sql = "INSERT INTO Login_details VALUES (%s,%s,%s,%s,%s,%s,%s)"
    c.execute(sql, (login_info[0],login_info[1],login_info[2],login_info[3],login_info[4],login_info[5],login_info[6]))
    conn.commit()
    return flask.render_template('successful_registration.html',is_logged_in=is_logged_in)

@app.route('/confirmuser',methods = ['POST','GET'])
def confirmuser():
    return flask.render_template('confirmuser.html',is_logged_in=is_logged_in)

@app.route('/forgot_password',methods = ['POST','GET'])
def forgot_password():
    if request.method == 'POST':
        user = request.form.to_dict()
        user=list(user.values())
    print(user)
    c,conn = connection()
    sql = "Select Passwd from Login_details where Email= %s "
    row_count = c.execute(sql, (user[0]))
    if row_count == 1:
        passwd = c.fetchone()[0]
        print("Password %s",passwd)
        conn.commit()
        msg = Message(subject = "Please find your Password in this email",
                  body = "Your Password is : %s" % passwd,
                  sender="bhaktimehta0909@gmail.com",
                  recipients=["%s"%user[0]])
        mail.send(msg)
        return flask.render_template('forgot_password.html',is_logged_in=is_logged_in)
    else:
        return flask.render_template('usernotfound.html',is_logged_in=is_logged_in)

