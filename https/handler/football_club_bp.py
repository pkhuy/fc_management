from flask import Blueprint, request, render_template, flash, redirect, jsonify
from flask_login import current_user
from service.manage_football_club import ManageFootballClub
from https.handler.auth_bp import token_required

football_club_bp = Blueprint("football_club_bp", __name__)

fc_service = ManageFootballClub()


@football_club_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            name = request.form["name"]
            quantity = request.form["quantity"]
            if not name:
                return "Missing fc name", 400
            if not quantity:
                return "Missing fc quantity", 400
            json_data = {
                "current_user_id": current_user.id,
                "name": name,
                "quantity": quantity
            }
            new_fc = fc_service.create(json_data)
            return render_template("response.html", context=new_fc)
        elif request.method == "GET":
            fcs = fc_service.read_all()
            fcs["entity"] = "football_clubs"
            return render_template("entity.html", context=fcs)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@football_club_bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "POST":
            if request.form["act"] == "Update":
                if not request.form["name"]:
                    return "Missing fc name", 400
                if not request.form["quantity"]:
                    return "Missing fc quantity", 400
                json_put_data = {
                    "id": id,
                    "name": request.form["name"],
                    "quantity": request.form["quantity"],
                    "current_user_id": current_user.id
                }
                update_result = fc_service.update(json_put_data)
                return render_template("response.html", context=update_result)
            elif request.form["act"] == "Join League":
                json_post_data = request.get_json()
                if not json_post_data["league_id"]:
                    return "Missing league id", 400
                json_post_data["fc_id"] = id
                create_league_com_result = fc_service.add_league_com(
                    json_post_data)
                return jsonify(create_league_com_result)
            elif request.form["act"] == "Create":
                delete_result = fc_service.delete({
                    "id": id,
                    "current_user_id": current_user.id,
                    "entity": "football_club"
                })
                return render_template("response.html", context=delete_result)
        else:
            fc = fc_service.read_by_id(id)
            fc["entity"] = "football_clubs"
            return render_template("manage.html", context=fc)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
