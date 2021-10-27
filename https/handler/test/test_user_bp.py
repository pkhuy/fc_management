from flask import Blueprint, request, render_template, flash, redirect
from flask.json import jsonify
from flask_login import current_user
from service.auth import Auth
from service.manage import Manage

user_bp = Blueprint("user_bp", __name__)


@user_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            id = request.form["id"]
            req = {
                "current_user": current_user,
                "entity": "user"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_user_by_id(id)
            }
            return redirect('/<id>')
        else:
            players = Manage().get_all_user()
            req = {
                "current_user": current_user,
                "entity": "user"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "entity": "users",
                "query": players,
                "data": Manage().get_user_by_id(1)
            }
            return render_template('entity.html', context=context)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@user_bp.route('/<int:id>', methods=['GET', 'POST', "PUT", "DELETE"])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "PUT":
            #get current user premission
            req = {
                "current_user": current_user,
                "entity": "user"
            }
            permissions = Manage().get_user_permission(req)
            print(current_user)
            context = {
                "current_user_id": current_user.id,
                "permissions": permissions,
                "data": Manage().get_user_by_id(id)
            }
            update_result = Manage().update_user(request.args)
            return jsonify(update_result)
        elif request.method == "DELETE":
            delete_result = Manage().delete_user(id)
            return jsonify(delete_result)
        else:
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "user"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_user_by_id(id)
            }
            return render_template('manage.html', context=context)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
'''
@user_bp.route('/create', methods=['GET', 'POST', "PUT", "DELETE"])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "POST":
            #get current user premission
            req = {
                "current_user": current_user,
                "entity": "user",
                "data": request.form
            }
            creatable = Manage().create_user() #manager insert user
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_user_by_id(id)
            }
            update_result = Manage().update_user(request.args)
            return jsonify(update_result)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
'''