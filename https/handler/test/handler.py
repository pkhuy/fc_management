from flask import Flask, request, render_template
from app import init_app
from service.auth import Auth
class Handler():
    @init_app.app.route('/', methods=['GET'])
    def home():
        try:
            return '''<h1>Distant Reading Archive</h1>
    <p>A prototype API for distant reading of science fiction novels.</p>'''
        except:
            return 1

    @init_app.app.route('/api/v1/login', methods=['GET', 'POST'])
    def login():
        if request.method == "POST":
            context = {
                "email": request.form['email'],
                "password": request.form['password']
            }

            return Auth.login(app, context)
        else:
            return render_template("login.html")
