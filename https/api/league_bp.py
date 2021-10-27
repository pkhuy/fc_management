from flask import Blueprint, request, render_template, flash, redirect
from flask.json import jsonify
from flask_login import current_user
from service.manage import Manage
from service.manage_league import ManageLeague

league_bp = Blueprint("league_bp", __name__)

league_service = ManageLeague()

@league_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            name = request.get_json()["name"]
            quantity = request.get_json()["quantity"]
            if not name:
                return "Missing league name", 400
            if not quantity:
                return "Missing league quantity", 400
            json_data = {
                "current_user_id": current_user.id,
                "name": name,
                "quantity": quantity
            }
            new_league = league_service.create(json_data)
            return jsonify(new_league)
        elif request.method == "GET":
            leagues = league_service.read_all()
            return jsonify(leagues)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@league_bp.route('/<int:id>', methods=['GET', 'POST'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "PUT":
            json_update_data = request.get_json()
            if not request.get_json()["name"]:
                return "Missing league name", 400
            if not request.get_json()["quantity"]:
                return "Missing league quantity", 400
            json_update_data["id"] = id
            update_result = league_service.update(json_update_data)
            return jsonify(update_result)
        elif request.method == "DELETE":
            delete_result = league_service.delete({
                "id": id,
                "current_user_id": current_user.id,
                "entity": "league"
            })
            return jsonify(delete_result)
        else:
            return jsonify(league_service.read_by_id(id))
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
