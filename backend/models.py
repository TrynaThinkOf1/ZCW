###################################
# user-auth-api/backend/models.py #
###################################

#==========================================================================#
#============================== DATABASES =================================#
#==========================================================================#

######################################
#          INITIALIZATION
#####################
# IMPORT LIBRARIES
from config import db
from datetime import datetime
######################################

######################################
#             DATABASES
#####################
class User(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    passkey = db.Column(db.String, nullable=False)
    # Personal Info
    email = db.Column(db.String)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    # User Info
    display_name = db.Column(db.String(25), nullable=False)
    path_to_pfp = db.Column(db.String, unique=True)
    bio = db.Column(db.String(120))
    website = db.Column(db.String)

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "display_name": self.display_name,
            "bio": self.bio,
            "website": self.website
        }
#####################
class VerificationCodes(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    code = db.Column(db.String, unique=True, nullable=False)
    time_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_json(self):
        return {
            "code": self.code,
            "time_created": self.time_created,
        }
#####################
class Post(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    poster = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    markdown_content = db.Column(db.String, nullable=False)
    num_likes = db.Column(db.Integer, nullable=False, default=0)

    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "poster": self.poster,
            "markdown_content": self.markdown_content,
            "num_likes": self.num_likes,
            "comments": self.comments,
        }

class Comment(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    poster_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    markdown_content = db.Column(db.String, nullable=False)
    num_likes = db.Column(db.Integer, nullable=False)