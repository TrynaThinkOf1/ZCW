#################################
# user-auth-api/backend/main.py #
#################################

#==========================================================================#
#======================== MAIN APP & ENDPOINTS ============================#
#==========================================================================#

######################################
#          INITIALIZATION
#####################
# IMPORT LIBRARIES
from flask import request, jsonify
import base64
import os

from config import app, db
from models import User
from verification import send_verify, check_verify
from utils import hash
######################################

######################################
#           POST ENDPOINT
#####################
@app.route('/api/user/create', methods=['POST'])
def create_user():
    passkey = hash.hashPasskey(request.form.get('passkey'))
    email = request.form.get('email')
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    display_name = request.form.get('displayName')

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"message": "Email already registered"}), 400

    user = User(first_name=first_name, last_name=last_name, email=email, passkey=passkey, display_name=display_name)
    db.session.add(user)
    db.session.flush()

    if request.files.get('pfp'):
        pfp = request.files.get('pfp')
        filepath = os.path.join("./files/pfps/", f"{user.id}.{pfp.filename.rsplit('.', 1)[-1]}")
        pfp.save(filepath)
        user.path_to_pfp = filepath

    db.session.commit()
    return user.to_json(), 201
######################################

######################################
#           GET ENDPOINT
#####################
@app.route('/api/user/get/<string:email>', methods=['GET'])
def get(email):
    user = User.query.filter_by(email=email).first()

    if hash.hashPasskey(request.form.get("passkey")) != user.passkey:
        return jsonify({"message": "Invalid Passkey"}), 401

    if not user:
        return jsonify({"message": "User not Found"}), 404

    try:
        with open(user.path_to_pfp, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        return jsonify({"message": "Failed to load profile picture", "error": str(e)}), 500

    return jsonify({
        "user": user.to_json(),
        "profile_picture": image_base64
    }), 200
######################################

######################################
#           PATCH ENDPOINT
#####################
@app.route('/api/user/update/<string:email>', methods=['PATCH'])
def update(email):
    user = User.query.filter_by(email=email).first()

    if hash.hashPasskey(request.form.get("passkey")) != user.passkey:
        return jsonify({"message": "Invalid Passkey"}), 401

    if not user:
        return jsonify({"message": "User not Found"}), 404

    if request.form.get("newPasskey") and request.form.get("newPasskey") != user.passkey:
        user.passkey = hash.hashPasskey(request.form.get("newPasskey"))
        db.session.commit()

    if request.form.get("newEmail") and request.form.get("newEmail") != user.email:
        user.email = request.form.get("newEmail")
        db.session.commit()

    if request.form.get("newFirstName") and request.form.get("newFirstName") != user.first_name:
        user.first_name = request.form.get("newFirstName")
        db.session.commit()

    if request.form.get("newLastName") and request.form.get("newLastName") != user.last_name:
        user.last_name = request.form.get("newLastName")
        db.session.commit()

    if request.form.get("newDisplayName") and request.form.get("newDisplayName") != user.display_name:
        user.display_name = request.form.get("newDisplayName")
        db.session.commit()

    if request.form.get("newBio") and request.form.get("newBio") != user.bio:
        user.bio = request.args.get("newBio")
        db.session.commit()

    if request.form.get("newWebsite") and request.form.get("newWebsite") != user.website:
        user.website = request.form.get("newWebsite")
        db.session.commit()

    if request.files.get("newPfp"):
        os.remove(user.path_to_pfp)
        pfp = request.files.get('newPfp')
        filepath = os.path.join("./files/pfps/", f"{user.id}.{pfp.filename.rsplit('.', 1)[-1]}")
        pfp.save(filepath)
        user.path_to_pfp = filepath
        db.session.commit()

    return jsonify({"user": user.to_json()}), 200
######################################

######################################
#          DELETE ENDPOINT
#####################
@app.route('/api/user/delete/<string:email>', methods=['DELETE'])
def delete(email):
    user = User.query.filter_by(email=email).first()

    if hash.hashPasskey(request.form.get("passkey")) != user.passkey:
        return jsonify({"message": "Invalid Passkey"}), 401

    if not user:
        return jsonify({"message": "User not Found"}), 404

    os.remove(user.path_to_pfp)

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User Deleted"}), 200
######################################

######################################
#      VERIFICATION ENDPOINTS
#####################
@app.route('/api/user/verify/<string:email>', methods=['POST'])
def verify(email):
    return send_verify(email)

@app.route('/api/code/verify/<string:code>', methods=['GET'])
def verify_code(code):
    if check_verify(code):
        return jsonify({"code": code}), 200

######################################
if __name__ == '__main__':
    with app.app_context():
        #db.drop_all() # uncomment to clear databases
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True) # ¡¡¡ DO NOT RUN ON DEBUG IN PROD !!!