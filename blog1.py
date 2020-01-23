import params as params  # importing parameters from 'config.json'
from flask import Flask, render_template, request, session, redirect
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import json

local_server = True  # when on local server
with open('config.json', 'r') as c:  # opening config.json as 'readable'
    params = json.load(c)["params"]  # parameters fetched as 'params'
app = Flask(__name__)  # Flask app
app.secret_key = "super-secret-key"  # secret key set
app.config['UPLOAD_FOLDER'] = params["upload_loc"]  # location for the uploader() function
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]  # connecting to phpMyAdmin(Xampp)
db = SQLAlchemy(app)


class Contacts(db.Model):  # defining the input details in our 'contact' page
    S_no = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    Email = db.Column(db.String(30), unique=True, nullable=False)
    Ph_num = db.Column(db.String(15), unique=True, nullable=False)
    Message = db.Column(db.String(80), unique=True, nullable=True)
    Date = db.Column(db.String(80), unique=True, nullable=False)


@app.route("/contact", methods=["GET", "POST"])  # route of 'contact'
def contact():  # for 'contact'
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        Ph_num = request.form.get("Ph_num")
        Message = request.form.get("Message")
        Date = request.form.get("Date")

        entry = Contacts(Name=name, Email=email, Ph_num=Ph_num, Message=Message, Date=Date)
        db.session.add(entry)  # the entry added onto our database
        db.session.commit()  # changes saved

    return render_template('contact.html', params=params)


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():  # for 'contact'
    if 'user' in session and session['user'] == params['user1']:  # check if user already logged in
        return render_template('login.html', params=params)
    if request.method == "POST":  # takes username and password typed by user
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if username == params['user1'] and userpass == params['pass1']:  # if username and password correct
            session['user'] = username
            return render_template('login.html', params=params)

    return render_template('dashboard.html', params=params)  # if username or password incorrect


@app.route("/")
def home():  # for 'homepage'
    return render_template('index.html', params=params)


@app.route("/uploader", methods=["GET", "POST"])
def uploader():  # for uploading files
    if 'user' in session and session['user'] == params['user1']:  # check if user already logged in
        if request.method == "POST":
            f = request.files('file1')
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "!! UPLOAD SUCCESSFUL !!"


@app.route('/logout')
def logout():  # for 'logout' button
    session['user'] = 0  # for removing keyerror:user
    session.pop('user')
    return redirect('/dashboard')  # return to 'dashboard'


@app.route("/about")
def about():  # for 'about'
    return render_template('about.html', params=params)


@app.route("/post")
def post():  # for 'post'
    return render_template('post.html', params=params)


app.run(debug=True)  # for running of app
# (debug=True) for reflecting changes made onto localhost
