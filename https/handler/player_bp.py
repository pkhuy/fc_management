from flask import Blueprint, jsonify, request, render_template, flash, redirect
from flask_login import current_user
from service.manage_player import ManagePlayer

player_bp = Blueprint("player_bp", __name__)

player_service = ManagePlayer()


@player_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            if not request.form["name"]:
                return "Missing player name", 400
            if not request.form["position"]:
                return "Missing player position", 400
            if not request.form["fc_id"]:
                return "Missing player fc_id", 400
            json_data = {
                "current_user_id": current_user.id,
                "name": request.form["name"],
                "position": request.form["position"],
                "fc_id": request.form["fc_id"]
            }
            new_player = player_service.create(json_data)
            return render_template("response.html", context=new_player)
        elif request.method == "GET":
            players = player_service.read_all()
            players["entity"] = "players"
            return render_template("entity.html", context=players)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@player_bp.route('/<int:id>', methods=['GET', 'POST'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "POST":
            if request.form["act"] == "Update":
                if not request.form["name"]:
                    return "Missing player name", 400
                if not request.form["position"]:
                    return "Missing player position", 400
                if not request.form["fc_id"]:
                    return "Missing player fc_id", 400
                json_update_data = {
                    "id": request.form["id"],
                    "name": request.form["position"],
                    "fc_id": request.form["fc_id"],
                    "current_user_id": current_user.id
                }
                update_result = player_service.update(json_update_data)
                return render_template("response.html", context=update_result)
            elif request.form["act"] == "Delete":
                delete_result = player_service.delete({
                    "id": id,
                    "current_user_id": current_user.id,
                    "entity": "player"
                })
                return render_template("response.html", context=delete_result)
        else:
            player = player_service.read_by_id(id)
            player["entity"] = "players"
            return render_template("manage.html", context=player)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
