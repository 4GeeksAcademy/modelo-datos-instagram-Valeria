from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60), nullable=False)
    firstname: Mapped[str] = mapped_column(String(40), nullable=False)
    lastname: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    post: Mapped[List["Post"]] = relationship("Post", back_populates="user")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")
    followers: Mapped[List["Follower"]] = relationship("Follower", back_populates="user_to")
    following: Mapped[List["Follower"]] = relationship("Follower", back_populates="user_from")


    def serialize(self):
        return {
            "id": self.id,
            "username":self.username,
            "firstname":self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "is_active": self.is_active
        }
    
    
class Follower(db.Model):

    __tablename__ = "followers"

    user_from_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    user_from: Mapped["User"] = relationship("User", back_populates="following")
    user_to: Mapped["User"] = relationship("User", back_populates="followers")

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }

class Post(db.Model):

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="post")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")
    media: Mapped[List["Media"]] = relationship("Media", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }

class Media(db.Model):

    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(40), nullable=False)
    url: Mapped[str] = mapped_column(String(200), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    post: Mapped["Post"] = relationship("Post", back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }
    
class Comment(db.Model):

    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(225), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id     
        }
