from flask import Flask, flash, request, jsonify, render_template, redirect, make_response
from service.auth import Auth, session
from flask_login import current_user, LoginManager, login_user, current_user, logout_user, login_required
from functools import wraps
from flask.blueprints import Blueprint
from itsdangerous import BadSignature
import jwt

secret_key = 'secretkey'

auth_bp = Blueprint("auth_bp", __name__, static_folder="static", template_folder="templates")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session["token"]
        print(token)
        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        try:
            data = jwt.decode(token, 'secretkey', algorithm="HS256")
            print(data)
        except jwt.ExpiredSignatureError:
            return False, 'Token has been expired. Please log in again.', {}
        except jwt.InvalidTokenError:
            return False, 'Invalid token. Please log in again.', {}
        except BadSignature:
            return False, 'invalid token', {}
        except:
            logout_user()
            return jsonify({"message": "Token is invalid"}), 403

        return f(*args, **kwargs)
    return decorated

@auth_bp.route('/unprotected')
def unprotected():
    return jsonify({"message": "Anyone can view this!"})

@auth_bp.route("/protected")
@token_required
def protected():
    return jsonify({"message": "Login pls!"})

@auth_bp.route("/", methods=['GET', 'POST'])
@auth_bp.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entity = request.form['entity']
        if entity =="User":
            return redirect('/users')
        if entity =="Group":
            return redirect('/groups')
        if entity =="Permission":
            return redirect('/permissions')
        if entity =="League":
            return redirect('/leagues')
        if entity =="FC":
            return redirect('/football_clubs')
        if entity =="Player":
            return redirect('/players')
    else:
        context = ('c', 'r', 'u', 'd')
        return render_template("home.html", permissions=context)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/home')
    if request.method == "POST":
        name = request.get_json()['name']
        email = request.get_json()['email']
        password = request.get_json()['password']
        if not name:
            return 'Missing Name', 401
        if not email:
            return 'Missing Email', 401
        if not password:
            return 'Missing Password', 401
        #chua format
        
        validate_email = Auth().check_email_existed(email)
        if validate_email:
            req = {
                "name": name,
                "email": email,
                "password": password,
            }
            res = Auth().register(req)
            return jsonify(res) #have not check yet
        else:
            flash('Regist Unsuccessful. This email has been used')
            return 'This email has existed', 400
        
    else:
        return "only POST method used", 500

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.get_json()['email']
        password = request.get_json()['password']
        if not email:
            return 'Missing Email', 401
        if not password:
            return 'Missing Password', 401

        res = Auth().login(request.get_json())
        login_user(res)
        
        flash('Login Unsuccessful. Please check email and password', 'danger')
        return "login successfully", 200
    else:
        return "Don't have that method. Pls try again", 500
    
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return "loged out"
