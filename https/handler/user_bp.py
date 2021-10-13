from flask import Blueprint, request, render_template, flash, redirect
from flask_login import current_user
from service.auth import Auth
from service.manage import Manage
user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/create', methods=['GET', 'POST'])
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
        permissions = Auth().get_user_permission(current_user)
        print(permissions)
        if "create" in permissions:
            return render_template('entity.html', context=1)
        else:
            flash("You have no permission to access!")
        return render_template('entity.html', context=1)

@user_bp.route('/entity', methods=['GET', 'POST'])
def entity():
    if request.method == "POST":
        context = {
            "user": current_user,
            "entity": request.form['entity']
        }
        #some func
        user_list = Manage().get_all_user()
        permissions = Auth().get_user_permission(current_user, context["entity"])
        print(permissions)
        return render_template('entity.html', permissions=permissions)
    else:
        permissions = Auth().get_user_permission(current_user)
        users = Manage().get_all_user()
        print(permissions, users)
        for user in users:
            print(user)
        context = {
            "permissions": permissions,
            "users": users
        }
        return render_template('entity.html', context=context)

@user_bp.route('/create', methods=['GET' , 'POST'])
@user_bp.route("/manage", methods=['GET', 'POST'])
def manage():
    context = ['r', 'u', 'd']
    return render_template('manage.html', permissions=context)
