from json import JSONEncoder
from flask import Flask, request, jsonify
from flask.json.provider import DefaultJSONProvider
from comments.database_setup import make_connection_string
from comments.models import db, json_serialize
from comments.views import auth, users, comments
from comments.views.auth import connect_login_manager


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        return json_serialize(obj)


def make_app():
    app = Flask(__name__, static_folder='../../static')
    connect_login_manager(app)
    app.json = CustomJSONProvider(app)
    app.secret_key = 'your-secret-key'
    app.config["SQLALCHEMY_DATABASE_URI"] = make_connection_string()
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(comments)
    db.init_app(app)
    return app


def cli():
    app = make_app()
    app.run(debug=True)
