
import flask
import os
import uuid
import jwt
import datetime
import requests
from bson import json_util, ObjectId
#from flask import request, Flask, render_template, Blueprint
from flask import (Flask,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for,
                   Blueprint)
from users.utils.users import list_users, add_user, delete_user, update_user, get_user_by_id, get_user_by_username
from decoratores.decoratores import login_required, token_required


users_blueprint = Blueprint('users', __name__)
@users_blueprint.route("/json", methods=["GET"])
@token_required
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
@token_required
def add_user_api():
    try:
        user = request.get_json()
        add_user(user)
        return {'status': 'success', 'message': 'User added successfully', 'data': json_util.dumps(user)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    

@users_blueprint.route("/delete/<id>", methods=["DELETE"])
@token_required
def delete_user_api(id):
    try:
        delete_user(id)
        return {'status': 'success', 'message': 'User deleted successfully'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@users_blueprint.route("/update/<id>", methods=["PUT"])
@token_required
def update_user_api(id):
    try:
        user = request.get_json()
        update_user(user_id=id, user=user)
        return {'status': 'success', 'message': 'User updated successfully', 'data': json_util.dumps(user)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@users_blueprint.route("/<id>", methods=["GET"])
@token_required
def get_user_api(id):

    try:
        user = get_user_by_id(id)
        user['_id'] = str(user['_id'])
        return {'status': 'success', 'message': 'User retrieved successfully', 'data':user}        
    except Exception as e:        
        return {'status': 'error', 'message': str(e)}

@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = get_user_by_username(username)
        if user and user["password"] == password:
            token = jwt.encode(
                {"username": username, 
                 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, 
                os.environ["SECRET_KEY"], 
                algorithm="HS256")
            response = requests.get("http://localhost:5000/users/json", headers={"Authorization": f"Bearer {token}"})
            return flask.jsonify(response.json())
    return render_template("login.html")
