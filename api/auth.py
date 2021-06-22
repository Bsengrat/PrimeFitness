from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from . import db
from .model import User, stat_weight

auth = Blueprint('auth', __name__)

global isLog
isLog = False

def isLogB(Log):
    Log = isLog
    return Log

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/login', methods=['POST'])
def login_POST():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))


@auth.route('/signup', methods= ['POST'])
def signup_POST():
    email = request.form.get('email')
    name = request.form.get('name')
    weight = request.form.get('weight')
    password = request.form.get('password')
    
    
    #checks password string to ensure its alpha numeric and between a certain amount of strings...
    pass_checker(password)


    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user:      
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # creates a new user...

    new_user = User(email=email, name=name, weight = weight, password=generate_password_hash(password, method='sha256'))



    #AgentRambo00
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    current_weight = stat_weight(Weight = weight, Stat_DATE = date.today())
    new_user.stat_weight.append(current_weight)
    db.session.add(current_weight)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():

    logout_user()
    isLog = False
    #return render_template('index.html', isLogin = isLog)
    return redirect(url_for('main.changeLog'))


def pass_checker(passw):
    plength = len(passw)

    #checks the length of the password...
    if plength < 5 or plength> 15:
        pcheck = False
        flash('There is either too few characters or far to many characters. Please enter password again...')
        return redirect(url_for('auth.signup'))
    
    #checks if the password has any speical characters in it...
    if passw.isalnum() == False:
        flash('There are special characters in this string. Please re-enter password...')
        return redirect(url_for('auth.signup'))



