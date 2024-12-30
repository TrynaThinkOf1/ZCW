#################################
# user-auth-api/backend/main.py #
#################################

#==========================================================================#
#======================= ACCOUNT APP & ENDPOINTS ==========================#
#==========================================================================#

######################################
#          INITIALIZATION
#####################
# IMPORT LIBRARIES
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import func
from werkzeug.utils import secure_filename
import base64
import os

from config import app, db
from models import User, Post, Comment
from verification import send_verify, check_verify, cleanup
from utils import hash, allowed_file
######################################

######################################
@app.route('/api/user/verify/<string:email>', methods=['GET'])
def verify(email: str):
    return jsonify(send_verify(email))

@app.route('/api/code/verify/<string:code>', methods=['POST'])
def verify_code(code):
    if not check_verify(code):
        return jsonify({"message": "Invalid code"}), 401

    passkey = hash.hashPasskey(request.json.get('passkey'))
    email = request.json.get('email')
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    display_name = request.json.get('displayName')

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"message": "Email already registered"}), 400

    user = User(first_name=first_name, last_name=last_name, email=email, passkey=passkey, display_name=display_name)
    db.session.add(user)
    db.session.flush()


    if 'pfp' in request.files:
        pfp = request.files['pfp']
        if pfp and allowed_file(pfp.filename):
            filename = secure_filename(pfp.filename)
            filepath = os.path.join("./files/pfps/", f"{user.id}.{filename.rsplit('.', 1)[-1]}")
            pfp.save(filepath)
            user.path_to_pfp = filepath
        else:
            return jsonify({"message": "Invalid file type"}), 400

    db.session.commit()

    token = create_access_token(identity={"id": user.id})

    return jsonify({"user": user.to_json(), "token": token}), 201
######################################

######################################
#           GET ENDPOINTS
#####################
@app.route('/api/user/get', methods=['POST'])
@jwt_required()
def get():
    jwt_id = get_jwt_identity()
    user = User.query.filter_by(id=jwt_id["id"]).first()
    if not user:
        return jsonify({"message": "User not Found"}), 404

    try:
        with open(user.path_to_pfp, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(e)
        print("returning default pfp")
        with open("./files/pfps/default.jpg", "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    return jsonify({"user": user.to_json(), "pfp": image_base64}), 200
@app.route('/api/user/login', methods=['POST'])
def login():
    email = request.json.get('email')
    passkey = hash.hashPasskey(request.json.get('passkey'))

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not Found"}), 404

    if passkey != user.passkey:
        return jsonify({"message": "Incorrect Passkey"}), 401

    try:
        with open(user.path_to_pfp, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(e)
        print("returning default pfp")
        with open("./files/pfps/default.jpg", "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    token = create_access_token(identity={"id": user.id})

    return jsonify({"user": user.to_json(), "token": token, "pfp": image_base64}), 200
######################################

######################################
#           PATCH ENDPOINT
#####################
@app.route('/api/user/update', methods=['PATCH'])
@jwt_required()
def update():
    jwt_id = get_jwt_identity()
    user = User.query.filter_by(id=jwt_id["id"]).first()
    if not user:
        return jsonify({"message": "User not Found"}), 404

    if request.json.get("newPasskey") and request.json.get("newPasskey") != user.passkey:
        user.passkey = hash.hashPasskey(request.json.get("newPasskey"))

    if request.json.get("newEmail") and request.json.get("newEmail") != user.email:
        user.email = request.json.get("newEmail")

    if request.json.get("newFirstName") and request.json.get("newFirstName") != user.first_name:
        user.first_name = request.json.get("newFirstName")

    if request.json.get("newLastName") and request.json.get("newLastName") != user.last_name:
        user.last_name = request.json.get("newLastName")

    if request.json.get("newDisplayName") and request.json.get("newDisplayName") != user.display_name:
        user.display_name = request.json.get("newDisplayName")

    if request.json.get("newBio") and request.json.get("newBio") != user.bio:
        user.bio = request.json.get("newBio")

    if request.json.get("newWebsite") and request.json.get("newWebsite") != user.website:
        user.website = request.json.get("newWebsite")

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

    if hash.hashPasskey(request.json.get("passkey")) != user.passkey:
        return jsonify({"message": "Invalid Passkey"}), 401

    if not user:
        return jsonify({"message": "User not Found"}), 404

    os.remove(user.path_to_pfp)

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User Deleted"}), 200
######################################

#==========================================================================#
#======================== FORUM APP & ENDPOINTS ===========================#
#==========================================================================#

@app.route('/api/post/create', methods=['POST'])
@jwt_required()
def post_create():
    jwt_id = get_jwt_identity()
    user = User.query.filter_by(id=jwt_id["id"]).first()
    if not user:
        return jsonify({"message": "User not Found"}), 404

    poster = user.id
    markdown_content = request.json.get("markdownContent")

    post = Post(poster=poster, markdown_content=markdown_content)
    db.session.add(post)
    db.session.commit()

    return jsonify({"post": post.to_json()}), 200

@app.route('/api/post/update', methods=['PATCH'])
@jwt_required()
def post_update():
    jwt_id = get_jwt_identity()
    user = User.query.filter_by(id=jwt_id["id"]).first()
    if not user:
        return jsonify({"message": "User not Found"}), 404

    new_markdown_content = request.json.get("markdownContent")
    if not new_markdown_content:
        return jsonify({"message": "Markdown Content Required"}), 401

    post_id = request.json.get("postId")
    post = Post.query.filter_by(id=post_id).first()
    post.markdown_content = new_markdown_content
    db.session.commit()

    return jsonify({"post": post.to_json()}), 200

@app.route('/api/post/delete/', methods=['DELETE'])
@jwt_required()
def post_delete():
    jwt_id = get_jwt_identity()
    user = User.query.filter_by(id=jwt_id["id"]).first()
    if not user:
        return jsonify({"message": "User not Found"}), 404

    post_id = request.json.get("postId")
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return jsonify({"message": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({"post": post.to_json()}), 200

@app.route('/api/post/get/<int:postid>', methods=['GET'])
@jwt_required()
def post_get(postid):
    post = Post.query.filter_by(id=postid).first()
    if not post:
        return jsonify({"message": "Post not found"}), 404

    return jsonify({"post": post.to_json()}), 200


@app.route('/api/feed/get', methods=['GET'])
@jwt_required()
def feed_get():
    posts = Post.query.order_by(func.random()).limit(50).all()

    return jsonify({"posts": posts}), 200

######################################
with app.app_context():
    #db.drop_all() # uncomment to clear databases
    db.create_all()
    cleanup()
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)  # ¡¡¡ DO NOT RUN ON DEBUG IN PROD !!!
