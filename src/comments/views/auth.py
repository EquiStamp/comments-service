from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import NoResultFound
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from comments.models import User, db


login_manager = LoginManager()


def connect_login_manager(app):
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    try:
        user = db.session.query(User).filter(User.email == data['email']).one()
    except NoResultFound:
        abort(401)

    if not user.check_password(data['password']):
        abort(403)

    login_user(user)
    return jsonify({"message": "logged in"})


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})


@auth.route('/profile', methods=['GET'])
@login_required
def profile():
    user_data = {field: getattr(current_user, field) for field in User.serializable_fields}
    return jsonify(user_data)
