import flask
from bson import json_util
from flask import request, Flask, render_template
from users.users import list_users, add_user, delete_user, update_user, get_user
from users.routes import users_blueprint

app = flask.Flask(__name__)
app.register_blueprint(users_blueprint, url_prefix="/users")

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)