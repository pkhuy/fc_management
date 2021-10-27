from flask import Blueprint
from flask_restful import Api

from https.api.auth_bp import auth_bp 
from https.api.football_club_bp import football_club_bp
from https.api.group_bp import group_bp
from https.api.league_bp import league_bp
from https.api.permission_bp import permission_bp
from https.api.player_bp import player_bp
from https.api.user_bp import user_bp
from https.handler.auth_bp import auth_bp as auth_ui
from https.handler.football_club_bp import football_club_bp as fc_ui
from https.handler.group_bp import group_bp as group_ui
from https.handler.league_bp import league_bp as league_ui
from https.handler.permission_bp import permission_bp as per_ui
from https.handler.player_bp import player_bp as player_ui
from https.handler.user_bp import user_bp as user_ui

api_bp = Blueprint("api", __name__, static_folder="static",
                   template_folder="templates")
api_bp.register_blueprint(auth_bp, url_prefix="/api/v1")
api_bp.register_blueprint(
    football_club_bp, url_prefix="/api/v1/football_clubs")
api_bp.register_blueprint(group_bp, url_prefix="/api/v1/groups")
api_bp.register_blueprint(league_bp, url_prefix="/api/v1/leagues")
api_bp.register_blueprint(permission_bp, url_prefix="/api/v1/permissions")
api_bp.register_blueprint(player_bp, url_prefix="/api/v1/players")
api_bp.register_blueprint(user_bp, url_prefix="/api/v1/users")

ui_bp = Blueprint("ui", __name__, static_folder="static",
                  template_folder="templates")
ui_bp.register_blueprint(auth_ui, url_prefix="")
ui_bp.register_blueprint(fc_ui, url_prefix="/football_clubs")
ui_bp.register_blueprint(group_ui, url_prefix="/groups")
ui_bp.register_blueprint(league_ui, url_prefix="/leagues")
ui_bp.register_blueprint(per_ui, url_prefix="/permissions")
ui_bp.register_blueprint(player_ui, url_prefix="/players")
ui_bp.register_blueprint(user_ui, url_prefix="/users")
