from config import db

class User(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    # Personal Info
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String, unique=True)
    phone_number = db.Column(db.String(10), unique=True)
    # User Info
    passkey = db.Column(db.String, nullable=False)
    path_to_pfp = db.Column(db.String, unique=True)
    display_name = db.Column(db.String(25), nullable=False)
    bio = db.Column(db.String(120))
    website = db.Column(db.String)

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "phoneNumber": self.phone_number,
            "displayName": self.display_name,
            "bio": self.bio,
            "website": self.website,
        }