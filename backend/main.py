from flask import request, jsonify
import base64

from config import app, db
from models import User

@app.route('/api/user/get/<string:email>', methods=['GET'])
def get(email):
    user = User.query.filter_by(email=email).first()

    if request.args.get("passkey") != user.passkey:
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

@app.route('/api/user/update/<string:email>', methods=['PATCH'])
def update(email):
    user = User.query.filter_by(email=email).first()

    if request.form.get("passkey") != user.passkey:
        return jsonify({"message": "Invalid Passkey"}), 401

    if not user:
        return jsonify({"message": "User not Found"}), 404

    if request.form.get("email") and request.form.get("email") != user.email:
        user.email = request.form.get("email")
        db.session.commit()

    if request.form.get("passkey") and request.form.get("passkey") != user.passkey:
        user.passkey = request.form.get("passkey")
        db.session.commit()

    if request.form.get("firstName") and request.form.get("firstName") != user.first_name:
        user.first_name = request.form.get("firstName")
        db.session.commit()

    if request.form.get("lastName") and request.form.get("lastName") != user.last_name:
        user.last_name = request.form.get("lastName")
        db.session.commit()

    if request.form.get("phoneNumber") and request.form.get("phoneNumber") != user.phone_number:
        user.phone_number = request.form.get("phoneNumber")
        db.session.commit()

    if request.form.get("displayName") and request.form.get("displayName") != user.display_name:
        user.display_name = request.form.get("displayName")
        db.session.commit()

    if request.form.get("bio") and request.form.get("bio") != user.bio:
        user.bio = request.args.get("bio")
        db.session.commit()

    if request.form.get("website") and request.form.get("website") != user.website:
        user.website = request.form.get("website")
        db.session.commit()

    return jsonify({"user": user.to_json()}), 200

if __name__ == '__main__':
    with app.app_context():
        #db.drop_all() # uncomment to clear databases
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True) # ¡¡¡ DO NOT RUN ON DEBUG IN PROD !!!