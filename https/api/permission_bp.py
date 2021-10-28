from flask import Blueprint, request, jsonify, render_template, flash, redirect
from flask_login import current_user
from service.manage_permission import ManagePermission

permission_bp = Blueprint("permission_bp", __name__)

per_service = ManagePermission()

@permission_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            if not request.get_json()["name"]:
                return "Missing permission name", 400
            if not request.get_json()["entity"]:
                return "Missing permission entity", 400
            json_data = {
                "current_user_id": current_user.id,
                "name": request.get_json()["name"]
            }
            new_per = per_service.create(json_data)
            return jsonify(new_per)
        elif request.method == "GET":
            pers = per_service.read_all()
            return jsonify(pers)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@permission_bp.route('/<int:id>', methods=['GET', 'POST', 'DELETE'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "PUT":
            json_update_data = request.get_json()
            if not request.get_json()["name"]:
                return "Missing permission name", 400
            if not request.get_json()["entity"]:
                return "Missing permission entity", 400
            json_update_data["id"] = id
            json_update_data["current_user_id"] = current_user.id
            update_result = per_service.update(json_update_data)
            return jsonify(update_result)
        elif request.method == "DELETE":
            delete_result = per_service.delete({
                "id": id,
                "current_user_id": current_user.id,
                "entity": "permission"
            })
            return jsonify(delete_result)
        else:
            return jsonify(per_service.read_by_id(id))
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
