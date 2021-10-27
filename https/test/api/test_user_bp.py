from flask import Blueprint, request, render_template, flash, redirect
from flask.json import jsonify
from flask_login import current_user
from service.manage_user import ManageUser

user_bp = Blueprint("user_bp", __name__)

user_service = ManageUser()

@user_bp.route('', methods=['GET'])
def entity():
    if current_user.is_authenticated:
        if request.method == "GET":
            users = user_service.read_all()
            return jsonify(users)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})

@user_bp.route('/<int:id>', methods=['GET', 'POST', "PUT", "DELETE"])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "PUT":
            json_update_data = request.get_json()
            if not request.get_json()["name"]:
                return "Missing user name", 400
            if not request.get_json()["email"]:
                return "Missing user email", 400
            if not request.get_json()["password"]:
                return "Missing user password", 400
            json_update_data["id"] = id
            json_update_data["current_user_id"] = current_user.id
            update_result = user_service.update(json_update_data)
            return jsonify(update_result)
        elif request.method == "DELETE":
            delete_result = user_service.delete({
                    "id": id,
                    "current_user_id": current_user.id,
                    "entity": "user"
                })
            return jsonify(delete_result)
        return jsonify(user_service.read_by_id(id))
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
