import cloudinary.uploader
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Profile

bp_profile = Blueprint('bp_profile', __name__)

@bp_profile.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    id = get_jwt_identity()
    user = User.query.get(id)
    return jsonify({"status": "success", "message": "Profile loaded",  "user": user.serialize()})

@bp_profile.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    file = None
    resp = None

    id = get_jwt_identity()
    user = User.query.get(id)
    
    if 'avatar' in request.files:
        file = request.files['avatar']
        if user.profile.public_id:
            resp = cloudinary.uploader.upload(file, public_id=user.profile.public_id)
        else:
            resp = cloudinary.uploader.upload(file, folder="profiles_users")


    user.profile.biography = request.form['biography'] if 'biography' in request.form else user.profile.biography
    user.profile.twitter = request.form['twitter'] if 'twitter' in request.form else user.profile.twitter
    user.profile.instagram = request.form['instagram'] if 'instagram' in request.form else user.profile.instagram
    user.profile.facebook = request.form['facebook'] if 'facebook' in request.form else user.profile.facebook
    user.profile.github = request.form['github'] if 'github' in request.form else user.profile.github
    user.profile.linkedin = request.form['linkedin'] if 'linkedin' in request.form else user.profile.linkedin

    user.profile.avatar = resp['secure_url'] if resp is not None else user.profile.avatar
    user.profile.public_id = resp['public_id'] if resp is not None else user.profile.public_id

    user.update()

    return jsonify({"status": "success", "message": "Profile updated!", "user": user.serialize() }), 200