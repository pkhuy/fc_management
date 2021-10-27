from flask import Blueprint, request, render_template, flash, redirect
from flask.json import jsonify
from flask_login import current_user
from service.auth import Auth
from service.manage import Manage

league_bp = Blueprint("league_bp", __name__)


@league_bp.route('', methods=['GET', 'POST'])
def entity():
    if current_user.is_authenticated:
        if request.method == "POST":
            id = request.form["id"]
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "league"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_league_by_id(id)
            }
            return redirect('/<id>')
            return render_template('manage.html', context=context)
        else:
            players = Manage().get_all_league()
            req = {
                "current_user": current_user,
                "entity": "league"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "entity": "leagues",
                "query": players,
                "data": Manage().get_league_by_id(1)
            }
            return render_template('entity.html', context=context)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@league_bp.route('/<int:id>', methods=['GET', 'POST'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "POST":
            id = request.form["id"]
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "league"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_league_by_id(id)
            }
            return redirect('/<int:id>')
            return render_template('manage.html', context=context)
        else:
            #some func
            valid_entry = isinstance(id, int)
            req = {
                "current_user": current_user,
                "entity": "league"
            }
            permissions = Manage().get_user_permission(req)
            context = {
                "permissions": permissions,
                "data": Manage().get_league_by_id(id)
            }
            return render_template('manage.html', context=context)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


'''
@player_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        context = {
            "current_user": current_user,
            "entity": request.form['entity']
        }
        #some func
        permissions = Auth().get_user_permission(current_user)
        return redirect('/manage')
    else:
        permissions = Auth().get_user_permission(current_user, )
        print(permissions)
        if "create" in permissions:
            return render_template('entity.html', context=1)
        else:
            flash("You have no permission to access!")
        return render_template('entity.html', context=1)



@player_bp.route("/manage", methods=['GET', 'POST'])
def manage():
    if request.method =="POST":
        pass
    else:
        context=1
        return render_template('manage.html', context=context)


@player_bp.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        pass
    else:
        propertise = Manage().get_entity_properties()
        context = 1
        return render_template('manage.html', context=context)
'''
