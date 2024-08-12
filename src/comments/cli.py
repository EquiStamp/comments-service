from json import JSONEncoder
from flask import Flask, request, jsonify
from flask.json.provider import DefaultJSONProvider
from comments.database_setup import make_connection_string
from comments.models import db, json_serialize
from comments.views import users, comments


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        return json_serialize(obj)


def make_app():
    app = Flask(__name__)
    app.json = CustomJSONProvider(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = make_connection_string()
    app.register_blueprint(users)
    app.register_blueprint(comments)
    db.init_app(app)
    return app


def cli():
    app = make_app()
    app.run(debug=True)
