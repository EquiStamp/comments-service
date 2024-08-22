from pathlib import Path
from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required
from sqlalchemy.exc import IntegrityError
from comments.models import User, db


users = Blueprint("users", __name__, url_prefix="/users")
AVATARS_PATH = Path(__file__).parent / 'avatars'
AVATARS_PATH.mkdir(parents=True, exist_ok=True)


@users.route("/", methods=["GET"])
def get_users():
    users = db.session.query(User).all()
    fields = request.args.get("fields") or 'id,username,display_name,email,avatar'
    fields = fields.split(",")
    users = [{field: getattr(u, field) for field in fields} for u in users]
    return jsonify(users), 200


@users.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if not (user := db.session.get(User, user_id)):
        return jsonify("No such user found"), 404

    fields = request.args.get("fields") or 'id,username,display_name,email,avatar'
    fields = fields.split(",")
    user = {field: getattr(user, field) for field in fields}
    return jsonify(user), 200


@users.route("/", methods=["POST"])
def create_user():
    data = request.get_json()

    for field in ['email', 'username', 'password', 'display_name']:
        if not data.get(field):
            return jsonify(f"'{field}' must be set"), 400

    try:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        return jsonify(str(e)), 400

    return jsonify(user.serialize()), 201


@users.route("/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id):
    if not (user := db.session.get(User, user_id)):
        return jsonify("No such user"), 404

    data = request.get_json()
    user.username = data.get("username", user.username)
    user.display_name = data.get("display_name", user.display_name)
    user.email = data.get("email", user.email)
    user.avatar = data.get("avatar", user.avatar)

    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(str(e)), 400

    return jsonify("Updated user"), 204


@users.route('/avatars/<path:img>', methods=["GET"])
def get_avatar(img):
    return send_file(AVATARS_PATH / img)
