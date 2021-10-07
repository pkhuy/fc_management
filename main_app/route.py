from flask import flash, redirect, config, request, make_response, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, url_for, flash, redirect, request
from main_app import app, db, bcrypt
from main_app.forms import RegistrationForm, LoginForm
from database.model import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('success.html')


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(form.email.data)
        print(user.email)
        print(user)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            #next_page = request.args.get('next')
            return redirect('/home')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/home')
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(name=form.name.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#api = Api(app)
#api.resource(HelloWorld, '/')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
