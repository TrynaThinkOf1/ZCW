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
######################################

######################################
#          USER DATABASE
#####################
class User(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    passkey = db.Column(db.String, nullable=False)
    # Personal Info
    email = db.Column(db.String)
    phone_number = db.Column(db.String(10), unique=True)
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
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "display_name": self.display_name,
            "bio": self.bio,
            "website": self.website
        }
######################################