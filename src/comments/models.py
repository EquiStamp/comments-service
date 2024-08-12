from typing import Collection
import uuid
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Text, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    backref,
    declarative_base,
    mapped_column,
    DeclarativeBase,
    relationship,
)
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    avatar = Column(String(200))
    comments = relationship("Comment", backref="user", lazy=True)


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    url = Column(String(200), nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    content = Column(Text, nullable=False)
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    replies = relationship(
        "Comment", backref=backref("parent", remote_side=[id]), lazy=True
    )
