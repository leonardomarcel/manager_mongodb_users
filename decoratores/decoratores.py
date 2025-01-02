from functools import wraps

from flask import (Flask,
                   redirect,
                   render_template_string,
                   request,
                   session,
                   url_for)

app = Flask(__name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("auth") is None:
            return redirect(url_for("users.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function