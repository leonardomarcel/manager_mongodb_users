import flask
from users.routes import users_blueprint
import os
from dotenv import load_dotenv

load_dotenv()
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.environ['MY_SECRET_KEY']
app.register_blueprint(users_blueprint, url_prefix="/users")

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)