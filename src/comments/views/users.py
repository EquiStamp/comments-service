from pathlib import Path
from flask import Blueprint, request, jsonify, send_file
from comments.models import User, db


users = Blueprint("users", __name__, url_prefix="/users")
AVATARS_PATH = Path(__file__).parent / 'avatars'
AVATARS_PATH.mkdir(parents=True, exist_ok=True)


@users.route("/", methods=["GET"])
def get_users():
    users = db.session.query(User).all()
    if fields := request.args.get("fields"):
        fields = fields.split(",")
        users = [{field: getattr(u, field) for field in fields} for u in users]
    return jsonify(users), 200


@users.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(
        username=data["username"],
        display_name=data["display_name"],
        email=data["email"],
        avatar=data.get("avatar", ""),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.id), 201


@users.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.username = data.get("username", user.username)
    user.display_name = data.get("display_name", user.display_name)
    user.email = data.get("email", user.email)
    user.avatar = data.get("avatar", user.avatar)
    db.session.commit()
    return "", 204


@users.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204


@users.route('/avatars/<path:img>', methods=["GET"])
def send_report(img):
    return send_file(AVATARS_PATH / img)
