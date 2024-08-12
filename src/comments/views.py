from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import markdown
import re
from comments.database_setup import make_connection_string
from comments.models import User, Comment

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = make_connection_string()
db = SQLAlchemy(app)


def is_valid_markdown(content):
    try:
        markdown.markdown(content)
        return True
    except:
        return False


@app.route("/users", methods=["POST"])
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


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.username = data.get("username", user.username)
    user.display_name = data.get("display_name", user.display_name)
    user.email = data.get("email", user.email)
    user.avatar = data.get("avatar", user.avatar)
    db.session.commit()
    return "", 204


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204


@app.route("/comments", methods=["POST"])
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


@app.route("/comments/<int:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()
    content = data.get("content", comment.content)
    if not is_valid_markdown(content):
        return jsonify(error="Invalid markdown"), 400
    comment.content = content
    db.session.commit()
    return "", 204


@app.route("/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return "", 204


@app.route("/comments/<int:comment_id>/upvote", methods=["POST"])
def upvote_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.upvotes += 1
    db.session.commit()
    return "", 204


@app.route("/comments/<int:comment_id>/downvote", methods=["POST"])
def downvote_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.downvotes += 1
    db.session.commit()
    return "", 204
