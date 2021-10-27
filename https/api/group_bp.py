from flask import Blueprint, request, render_template, flash, redirect
from flask.json import jsonify
from flask_login import current_user
from service.manage_group import ManageGroup

group_bp = Blueprint("group_bp", __name__)

group_service = ManageGroup()

@group_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            if not request.get_json()["name"]:
                return "Missing group name", 400
            json_data = {
                "current_user_id": current_user.id,
                "name": request.get_json()["name"]
            }
            new_group = group_service.create(json_data)
            return jsonify(new_group)
        elif request.method == "GET":
            groups = group_service.read_all()
            return jsonify(groups)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@group_bp.route('/<int:id>', methods=['GET', 'POST'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "PUT":
            json_update_data = request.get_json()
            if not request.get_json()["name"]:
                return "Missing group name", 400
            json_update_data["id"] = id
            json_update_data["current_user_id"] = current_user.id
            update_result = group_service.update(json_update_data)
            return jsonify(update_result)
        elif request.method == "DELETE":
            delete_result = group_service.delete({
                "id": id,
                "current_user_id": current_user.id,
                "entity": "group"
            })
            return jsonify(delete_result)
        else:
            return jsonify(group_service.read_by_id(id))
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
