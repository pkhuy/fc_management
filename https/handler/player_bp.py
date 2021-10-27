from flask import Blueprint, request, render_template, flash, redirect
from flask import json
from flask.helpers import url_for
from flask.json import jsonify
from flask_login import current_user
from service.auth import Auth
from service.manage import Manage

player_bp = Blueprint("player_bp", __name__)


@player_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            '''req = {
                "name": request.args["name"],
                "position": request.args["position"],
                "fc_id": request.args["fc_id"]
            }'''
            new_player = Manage().create_player(request.form)
            return jsonify(new_player)
        else:
            players = Manage().get_all_player()
            req = {
                "current_user": current_user,
                "entity": "player"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "entity": "players",
                "query": players,
                "data": Manage().get_player_by_id(3)
            }
            return render_template('entity.html', context=context)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@player_bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "PUT":
            #not use and valid yet
            req = {
                "current_user": current_user,
                "entity": "player"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_player_by_id(id)
            }
            print(request.args)
            update_result = Manage().update_player(request.args)
            return jsonify(update_result)
        elif request.method == "POST":
            #not use and valid yet
            req = {
                "current_user": current_user,
                "entity": "player"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_player_by_id(id)
            }
            print(request.args)
            update_result = Manage().update_player(request.args)
            return jsonify(update_result)
            return redirect(url_for('entity'))
        elif request.method == "DELETE":
            delete_result = Manage().delete_player(id)
            return jsonify(delete_result)
        else:
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "player"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "entity": "players",
                "data": Manage().get_player_by_id(id)
            }

            return render_template('manage.html', context=context)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
