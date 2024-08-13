from flask import Blueprint, request, jsonify
from comments.models import User, Comment, db, json_serialize


users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/", methods=["GET"])
def get_users():
    return jsonify(db.session.query(User).all()), 200


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
