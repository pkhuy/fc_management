from flask import Blueprint, jsonify, request, render_template, flash, redirect
from flask_login import current_user
from service.manage_player import ManagePlayer

player_bp = Blueprint("player_bp", __name__)

player_service = ManagePlayer()

@player_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            if not request.get_json()["name"]:
                return "Missing player name", 400
            if not request.get_json()["position"]:
                return "Missing player position", 400
            if not request.get_json()["fc_id"]:
                return "Missing player fc_id", 400
            json_data = {
                "current_user_id": current_user.id,
                "name": request.get_json()["name"],
                "position": request.get_json()["position"],
                "fc_id": request.get_json()["fc_id"]
            }
            new_player = player_service.create(json_data)
            return jsonify(new_player)
        elif request.method == "GET":
            players = player_service.read_all()
            return jsonify(players)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})

@player_bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "PUT":
            json_update_data = request.get_json()
            if not request.get_json()["name"]:
                return "Missing player name", 400
            if not request.get_json()["position"]:
                return "Missing player position", 400
            if not request.get_json()["fc_id"]:
                return "Missing player fc_id", 400
            json_update_data["id"] = id
            json_update_data["current_user_id"] = current_user.id
            update_result = player_service.update(json_update_data)
            return jsonify(update_result)
        elif request.method == "DELETE":
            delete_result = player_service.delete({
                "id": id,
                "current_user_id": current_user.id,
                "entity": "player"
            })
            return jsonify(delete_result)
        else:
            return jsonify(player_service.read_by_id(id))
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
