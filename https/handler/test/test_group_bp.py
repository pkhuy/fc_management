from flask import Blueprint, request, render_template, flash, redirect
from flask.json import jsonify
from flask_login import current_user
from service.auth import Auth
from service.manage import Manage

group_bp = Blueprint("group_bp", __name__)


@group_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            id = request.form["id"]
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "group"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_group_by_id(id)
            }
            return redirect('/<id>')
            return render_template('manage.html', context=context)
        else:
            groups = Manage().get_all_group()
            req = {
                "current_user": current_user,
                "entity": "group"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "entity": "groups",
                "query": groups,
                "data": Manage().get_group_by_id(1)
            }
            return render_template('entity.html', context=context)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@group_bp.route('/<int:id>', methods=['GET', 'POST'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "POST":
            id = request.form["id"]
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "group"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_group_by_id(id)
            }
            return redirect('/<int:id>')
            return render_template('manage.html', context=context)
        else:
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "group"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_group_by_id(id)
            }
            return render_template('manage.html', context=context)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
