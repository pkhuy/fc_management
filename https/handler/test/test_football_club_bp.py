from flask import Blueprint, request, render_template, flash, redirect, jsonify
from flask_login import current_user
from service.auth import Auth
from service.manage import Manage

football_club_bp = Blueprint("football_club_bp", __name__)


@football_club_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            id = request.form["id"]
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "football_club"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_football_club_by_id(id)
            }
            return redirect('/<id>')
            return render_template('manage.html', context=context)
        else:
            football_club = Manage().get_all_football_club()
            req = {
                "current_user": current_user,
                "entity": "football_club"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "entity": "football_clubs",
                "query": football_club,
                "data": Manage().get_football_club_by_id(1)
            }
            return render_template('entity.html', context=context)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@football_club_bp.route('/<int:id>', methods=['GET', 'POST'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "PUT":
            #not use and valid yet
            req = {
                "current_user": current_user,
                "entity": "football_club"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_football_club_by_id(id)
            }
            print(request.args)
            update_result = Manage().update_football_club(request.args)
            return jsonify(update_result)
        elif request.method == "DELETE":
            delete_result = Manage().delete_football_club(id)
            return jsonify(delete_result)
        else:
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "football_club"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "entity": "football_club",
                "data": Manage().get_football_club_by_id(id)
            }
            return render_template('manage.html', context=context)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
