from flask import Blueprint, request, jsonify, render_template, flash, redirect
from flask_login import current_user
from service.manage_permission import ManagePermission

permission_bp = Blueprint("permission_bp", __name__)

per_service = ManagePermission()


@permission_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            if not request.form["name"]:
                return "Missing permission name", 400
            if not request.form["entity"]:
                return "Missing permission entity", 400
            json_data = {
                "current_user_id": current_user.id,
                "name": request.form["name"],
                "entity": request.form["entity"]
            }
            new_per = per_service.create(json_data)
            return render_template("response.html", context=new_per)
        elif request.method == "GET":
            pers = per_service.read_all()
            pers["entity"] = "permissions"
            return render_template("entity.html", context=pers)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@permission_bp.route('/<int:id>', methods=['GET', 'POST', 'DELETE'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "POST":
            if request.form["act"] == "Create":
                if not request.form["name"]:
                    return "Missing permission name", 400
                if not request.form["entity"]:
                    return "Missing permission entity", 400
                json_update_data = {
                    "id": id,
                    "name": request.form["name"],
                    "entity": request.form["entity"],
                    "current_user_id": current_user.id
                }
                create_result = per_service.create(json_update_data)
                return render_template("response.html", context=create_result)
            elif request.form["act"] == "Delete":
                delete_result = per_service.delete({
                    "id": id,
                    "current_user_id": current_user.id,
                    "entity": "permission"
                })
                return render_template("response.html", context=delete_result)
        else:
            per = per_service.read_by_id(id)
            per["entity"] = "permissions"
            return render_template("manage.html", context=per)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
