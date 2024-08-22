import json
import uuid
import logging
from decimal import Decimal
from sqlalchemy import Column, ForeignKey, String, Integer, Text
from sqlalchemy.orm import backref, DeclarativeBase, relationship
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)


def json_serialize(obj):
    """JSON serializer for objects not serializable by default json code, including SQLAlchemy ORM objects."""

    # Function to serialize a single object
    def serialize_single_object(single_obj):
        # Check if the object is a basic data type
        if isinstance(single_obj, (int, float, bool, str)):
            return single_obj
        elif isinstance(single_obj, Decimal):
            return float(single_obj)
        elif isinstance(single_obj, dict):
            return {
                serialize_single_object(key): serialize_single_object(value)
                for key, value in single_obj.items()
                if value is not None
            }
        elif isinstance(single_obj, list):
            return [
                serialize_single_object(item) for item in single_obj if item is not None
            ]
        elif hasattr(single_obj, "__table__"):  # Check if it's a SQLAlchemy ORM object
            return serialize_single_object(single_obj.serialize())
        else:
            # Default serialization for other types
            return str(single_obj)

    # Serialize a list of objects or a single object
    return serialize_single_object(obj)


class Base(DeclarativeBase):
    serializable_fields = ["id"]

    def serialize(self, serialize_children=True):
        def as_serializable(field, serialize_children=True):
            if field in self.__mapper__.relationships and not serialize_children:
                return None

            try:
                val = getattr(self, field, None)
            except KeyError:
                logger.error(
                    "Could not extract value from ORM model: %s, %s", field, self
                )
                return None

            # if it's a child ORM model, and this is the first layer, serialize it. Otherwise
            # just return None, to avoid pulling the whole database
            if hasattr(val, "__table__"):
                return (
                    val.serialize(serialize_children=False)
                    if serialize_children
                    else None
                )
            if isinstance(val, Decimal):
                return float(val)
            if (
                isinstance(val, (list, tuple))
                and field in self.__mapper__.relationships
            ):
                return [child.serialize(False) for child in val]
            if isinstance(val, (list, tuple)):
                return [json_serialize(child) for child in val]
            if isinstance(val, uuid.UUID):
                return str(val)

            try:
                json.dumps(val)
                return val
            except TypeError:
                return str(val)

        vals = {field: as_serializable(field) for field in self.serializable_fields}
        return {k: v for k, v in vals.items() if v is not None}


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "user"

    serializable_fields = [
        "id",
        "username",
        "display_name",
        "email",
        "avatar",
        "comments",
    ]

    id = Column(Integer, primary_key=True)
    password = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    avatar = Column(String(200))
    comments = relationship("Comment", backref="user", lazy=True)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def check_password(self, password):
        return self.password == password


class Comment(Base):
    __tablename__ = "comment"
    serializable_fields = [
        "id",
        "url",
        "parent_id",
        "user_id",
        "content",
        "upvotes",
        "downvotes",
        "replies",
    ]

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("comment.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    content = Column(Text, nullable=False)
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    replies = relationship(
        "Comment", backref=backref("parent", remote_side=[id]), lazy=True
    )


db = SQLAlchemy(model_class=Base)
