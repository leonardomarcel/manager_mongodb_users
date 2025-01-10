from functools import wraps
import jwt
import os
from flask import (Flask,
                   redirect,
                   render_template_string,
                   request,
                   session,
                   jsonify,
                   url_for)

app = Flask(__name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if session.get("auth") is None:
            return redirect(url_for("users.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization").split()[1]
        try:
            jwt.decode(token, os.environ["SECRET_KEY"], algorithms=["HS256"])
        except Exception as e:
            return jsonify({
                "NOK": "Token is invalid or expired",
                "message": str(e),
                "token": token
            }), 401
            
        return f(*args, **kwargs)

    return decorated_function

    