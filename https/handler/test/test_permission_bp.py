from flask import Blueprint, request, jsonify, render_template, flash, redirect
from flask_login import current_user
from service.auth import Auth
from service.manage import Manage
permission_bp = Blueprint("permission_bp", __name__)


@permission_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            id = request.form["id"]
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "permission"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_permission_by_id(id)
            }
            return redirect('/<id>')
            return render_template('manage.html', context=context)
        else:
            permissions = Manage().get_all_permission()
            req = {
                "current_user": current_user,
                "entity": "permission"
            }
            user_permissions = Manage().get_user_permission(req)
            context = {
                "permissions": user_permissions,
                "entity": "permissions",
                "query": permissions,
                "data": Manage().get_permission_by_id(1)
            }
            return render_template('entity.html', context=context)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@permission_bp.route('/<int:id>', methods=['GET', 'POST'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "POST":
            id = request.form["id"]
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "permission"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_permission_by_id(id)
            }
            return redirect('/<int:id>')
            return render_template('manage.html', context=context)
        else:
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "permission"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_permission_by_id(id)
            }
            return render_template('manage.html', context=context)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
