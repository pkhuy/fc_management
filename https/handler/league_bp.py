from os import name
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
            name = request.form["name"]
            quantity = request.form["quantity"]
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
            return render_template("response.html", context=new_league)
        elif request.method == "GET":
            leagues = league_service.read_all()
            leagues["entity"] = "leagues"
            return render_template("entity.html", context=leagues)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@league_bp.route('/<int:id>', methods=['GET', 'POST'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "POST":
            if request.form["act"] =="Update":
                if not request.form["name"]:
                    return "Missing league name", 400
                if not request.form["quantity"]:
                    return "Missing league quantity", 400
                json_update_data = {
                    "id": id,
                    "name": request.form["name"],
                    "quantity": request.form["quantity"],
                    "current_user_id": current_user.id
                }
                update_result = league_service.update(json_update_data)
                return render_template("response.html", context=update_result)
            elif request.form["act"] == "Delete":
                delete_result = league_service.delete({
                    "id": id,
                    "current_user_id": current_user.id,
                    "entity": "league"
                })
                return render_template("response.html", context=delete_result)
        else:
            league = league_service.read_by_id(id)
            league["entity"] = "leagues"
            return render_template("manage.html", context=league)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
