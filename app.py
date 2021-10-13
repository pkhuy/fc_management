from flask import Flask, flash, request, jsonify, render_template, redirect
from service.auth import Auth
from service.manage import Manage
from flask_login import current_user, LoginManager, login_user, current_user, logout_user, login_required
from https.handler.auth_bp import auth_bp
from https.handler.user_bp import user_bp
from https.handler.group_bp import group_bp
from https.handler.league_bp import league_bp
from https.handler.permission_bp import permission_bp
from https.handler.player_bp import player_bp
from https.handler.fc_bp import fc_bp

def init_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.register_blueprint(auth_bp, url_prefix="")
    app.register_blueprint(fc_bp, url_prefix="/fc")
    app.register_blueprint(group_bp, url_prefix="/group")
    app.register_blueprint(league_bp, url_prefix="/league")
    app.register_blueprint(permission_bp, url_prefix="/permission")
    app.register_blueprint(player_bp, url_prefix="/player")
    app.register_blueprint(user_bp, url_prefix="/user")
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Auth().loaded_user(user_id)

    app.run()

if __name__ == '__main__':
    init_app()
