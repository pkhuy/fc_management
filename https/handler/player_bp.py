from flask import Blueprint, request, render_template, flash, redirect
from flask_login import current_user
from service.auth import Auth
from service.manage import Manage
player_bp = Blueprint("player_bp", __name__)


@player_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        context = {
            "current_user": current_user,
            "entity": request.form['entity']
        }
        #some func
        permissions = Auth().get_user_permission(current_user)
        return redirect('/manage')
    else:
        permissions = Auth().get_user_permission(current_user)
        print(permissions)
        if "create" in permissions:
            return render_template('entity.html', context=1)
        else:
            flash("You have no permission to access!")
        return render_template('entity.html', context=1)


@player_bp.route('/entity', methods=['GET', 'POST'])
def entity():
    if request.method == "POST":
        context = {
            "user": current_user,
            "entity": request.form['entity']
        }
        #some func
        user_list = Manage().get_all_user()
        permissions = Auth().get_user_permission(
            current_user, context["entity"])
        print(permissions)
        return render_template('entity.html', permissions=permissions)
    else:
        
        players = Manage().get_all_player()
        req = {
            "current_user": current_user,
            "entity": "player"
        }
        permissions = Manage().get_user_permission(req)
        context = {
            "permissions": permissions,
            "players": players
        }
        return render_template('entity.html', context=context)


@player_bp.route('/create', methods=['GET', 'POST'])
@player_bp.route("/manage", methods=['GET', 'POST'])
def manage():
    context = ['r', 'u', 'd']
    return render_template('manage.html', permissions=context)
