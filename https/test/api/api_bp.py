from flask import Flask, flash, request, jsonify, render_template, redirect, make_response
from service.auth import Auth
import jwt
import datetime
from flask_login import current_user, LoginManager, login_user, current_user, logout_user, login_required
from functools import wraps
from flask.blueprints import Blueprint

secret_key = '5791628bb0b13ce0c676dfde280ba245'

api_bp = Blueprint("api_bp", __name__,
                    static_folder="static", template_folder="templates")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        try:
            data = jwt.decode(token, secret_key)
        except:
            logout_user()
            return jsonify({"message": "Token is invalid"}), 403

        return f(*args, **kwargs)
    return decorated


@api_bp.route('/unprotected')
def unprotected():
    return jsonify({"message": "Anyone can view this!"})


@api_bp.route("/protected")
@token_required
def protected():
    return jsonify({"message": "Login pls!"})


@api_bp.route("/", methods=['GET', 'POST'])
@api_bp.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entity = request.form['entity']
        if entity == "User":
            return redirect('/users')
        if entity == "Group":
            return redirect('/groups')
        if entity == "Permission":
            return redirect('/permissions')
        if entity == "League":
            return redirect('/leagues')
        if entity == "FC":
            return redirect('/football_clubs')
        if entity == "Player":
            return redirect('/players')
    else:
        context = ('c', 'r', 'u', 'd')
        return render_template("home.html", permissions=context)


@api_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/home')
    if request.method == "POST":
        req = {
            "name": request.form["name"],
            "email": request.form['email'],
            "password": request.form['password'],
        }
        validate_email = Auth().check_email_existed(req["email"])
        if validate_email:
            res = Auth().register(req)
            return redirect('/login')
        else:
            flash('Regist Unsuccessful. This email has been used')
            return redirect('/register')
    else:
        return render_template("register.html")


@api_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        req = {
            "email": request.form['email'],
            "password": request.form['password']
        }

        res = Auth().login(req)

        if res['success']:
            login_user(res['data'][0])
            token = jwt.encode({
                "email": req["email"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
                secret_key
            )

            return jsonify({"token": token})
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        return render_template("login.html")


@api_bp.route("/logout")
def logout():
    logout_user()
    return redirect('/')
