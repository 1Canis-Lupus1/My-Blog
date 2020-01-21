import params as params
from flask import Flask, render_template, request,session,redirect
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import json

local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
app.secret_key="super-secret-key"
app.config['UPLOAD_FOLDER']=params["upload_loc"]
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
db = SQLAlchemy(app)

class Contacts(db.Model):
    S_no = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    Email = db.Column(db.String(30), unique=True, nullable=False)
    Ph_num = db.Column(db.String(15), unique=True, nullable=False)
    Message = db.Column(db.String(80), unique=True, nullable=True)
    Date = db.Column(db.String(80), unique=True, nullable=False)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        Ph_num = request.form.get("Ph_num")
        Message = request.form.get("Message")
        Date = request.form.get("Date")

        entry = Contacts(Name=name, Email=email, Ph_num=Ph_num, Message=Message, Date=Date)
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html', params=params)

@app.route('/dashboard',methods=["GET","POST"])
def dashboard():
    if ('user' in session and session['user']==params['user1']):  #check if user already logged in
        return render_template('login.html', params=params)
    if (request.method=="POST"):    #takes username and password typed by user
        username=request.form.get('uname')
        userpass=request.form.get('pass')
        if(username==params['user1'] and userpass==params['pass1']):   #if username and password correct
            session['user']=username
            return render_template('login.html',params=params)

    return render_template('dashboard.html',params=params)

@app.route("/")
def home():
    return render_template('index.html', params=params)

@app.route("/uploader",methods=["GET","POST"])
def uploader():
    if ('user' in session and session['user'] == params['user1']):
        if(request.method=="POST"):
            f=request.files('file1')
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
            return "!! UPLOAD SUCCESSFULL !!"

@app.route('/logout')
def logout():
    session['user']=0 #for removing keyerror:user
    session.pop('user')
    return redirect('/dashboard')

@app.route("/about")
def about():
    return render_template('about.html', params=params)

@app.route("/post")
def post():
    return render_template('post.html', params=params)

app.run(debug=True)
