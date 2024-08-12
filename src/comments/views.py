from flask import Blueprint, request, jsonify
import markdown
from comments.models import User, Comment, db, json_serialize


def is_valid_markdown(content):
    try:
        markdown.markdown(content)
        return True
    except:
        return False


comments = Blueprint("comments", __name__, url_prefix="/comments")
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


@comments.route("/", methods=["POST"])
def create_comment():
    data = request.get_json()
    content = data["content"]
    if not is_valid_markdown(content):
        return jsonify(error="Invalid markdown"), 400
    comment = Comment(
        url=data["url"],
        parent_id=data.get("parent_id"),
        user_id=data["user_id"],
        content=content,
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.id), 201


@comments.route("/<int:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()
    content = data.get("content", comment.content)
    if not is_valid_markdown(content):
        return jsonify(error="Invalid markdown"), 400
    comment.content = content
    db.session.commit()
    return "", 204


@comments.route("/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return "", 204


@comments.route("/<int:comment_id>/upvote", methods=["POST"])
def upvote_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.upvotes += 1
    db.session.commit()
    return "", 204


@comments.route("/<int:comment_id>/downvote", methods=["POST"])
def downvote_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.downvotes += 1
    db.session.commit()
    return "", 204
