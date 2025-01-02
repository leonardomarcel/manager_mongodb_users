
import flask
from bson import json_util
#from flask import request, Flask, render_template, Blueprint
from flask import (Flask,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for,
                   Blueprint)
from users.users import list_users, add_user, delete_user, update_user, get_user_by_id, get_user_by_username
from decoratores.decoratores import login_required

users_blueprint = Blueprint('users', __name__)
@users_blueprint.route("/json", methods=["GET"])
def get_users():
    users = list_users() 
    return flask.jsonify(users)

@users_blueprint.route("/", methods=["GET"])
@login_required
def home():
    users = list_users() 
    return render_template("base.html", title="Flask", users=users)

@users_blueprint.route("/status")
def status():
    return render_template("base.html", title="Status")


@users_blueprint.route("/add", methods=["POST"])
def add_user_api():
    try:
        user = request.get_json()
        add_user(user)
        return {'status': 'success', 'message': 'User added successfully', 'data': json_util.dumps(user)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    

@users_blueprint.route("/delete/<id>", methods=["DELETE"])
def delete_user_api(id):
    try:
        delete_user(id)
        return {'status': 'success', 'message': 'User deleted successfully'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@users_blueprint.route("/update/<id>", methods=["PUT"])
def update_user_api(id):
    try:
        user = request.get_json()
        update_user(user_id=id, user=user)
        return {'status': 'success', 'message': 'User updated successfully', 'data': json_util.dumps(user)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@users_blueprint.route("/<id>", methods=["GET"])
def get_user_api(id):
    try:
        user = get_user_by_id(id)
        return {'status': 'success', 'message': 'User retrieved successfully', 'data': json_util.dumps(user)}        
    except Exception as e:        
        return {'status': 'error', 'message': str(e)}

@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = get_user_by_username(username)
        if user and user["password"] == password:
            session["username"] = username
            session["auth"] = True
            return redirect(url_for("users.home"))
    return render_template("login.html")
