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
            if not request.form["name"]:
                return "Missing group name", 400
            json_data = {
                "current_user_id": current_user.id,
                "name": request.form["name"]
            }
            new_group = group_service.create(json_data)
            return render_template("response.html", context=new_group)
        elif request.method == "GET":
            groups = group_service.read_all()
            groups["entity"] = "groups"
            return render_template("entity.html", context=groups)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@group_bp.route('/<int:id>', methods=['GET', 'POST', 'DELETE'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "POST":
            if request.form["act"] == "Update":
                if not request.form["name"]:
                    return "Missing group name", 400
                json_update_data = {
                    "id": id,
                    "name": request.form["name"],
                    "current_user_id": current_user.id
                }
                update_result = group_service.update(json_update_data)
                return render_template("response.html", context=update_result)
            elif request.method == "DELETE":
                delete_result = group_service.delete({
                    "id": id,
                    "current_user_id": current_user.id,
                    "entity": "group"
                })
                return render_template("response.html", context=delete_result)
        else:
            group = group_service.read_by_id(id)
            group["entity"] = "groups"
            return render_template("manage.html", context=group)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
