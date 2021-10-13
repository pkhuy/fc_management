from flask import Flask, flash, request, jsonify, render_template, redirect
from service.auth import Auth
from service.manage import Manage
from flask_login import current_user, LoginManager, login_user, current_user, logout_user, login_required

from flask.blueprints import Blueprint

auth_bp = Blueprint("auth_bp", __name__, static_folder="static", template_folder="templates")


@auth_bp.route("/", methods=['GET', 'POST'])
@auth_bp.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entity = request.form['entity']
        if entity =="User":
            return redirect('/user/entity')
        if entity =="Group":
            return redirect('/group/entity')
        if entity =="Permission":
            return redirect('/permission/entity')
        if entity =="League":
            return redirect('/league/entity')
        if entity =="FC":
            return redirect('/fc/entity')
        if entity =="Player":
            return redirect('/player/entity')
        
    context = ('c', 'r', 'u', 'd')
    return render_template("home.html", permissions=context)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/home')
    if request.method == "POST":
        req = {
            "email": request.form['email'],
            "password": request.form['password'],
        }
        res = Auth().register(req)
        return redirect('/login')
    else:
        return render_template("register.html")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        req = {
            "email": request.form['email'],
            "password": request.form['password']
        }
        res = Auth().login(req)

        if res['success']:
            login_user(res['data'][0])
            return redirect('/')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect('/login')
    else:
        return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect('/')
