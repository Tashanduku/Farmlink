from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from ..models import db, User, UserFollow
from ..error_handlers import ValidationError, NotFoundError
from ..schemas import UserSchema, user_schema
from marshmallow.exceptions import ValidationError as MarshmallowValidationError

user_bp = Blueprint('users', __name__)

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    
    # Get follower and following counts
    follower_count = UserFollow.query.filter_by(followed_id=user_id).count()
    following_count = UserFollow.query.filter_by(follower_id=user_id).count()
    
    return jsonify({
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'bio': user.bio,
        'location': user.location,
        'expertise': user.expertise,
        'is_expert': user.is_expert,
        'profile_picture': user.profile_picture,
        'created_at': user.created_at,
        'follower_count': follower_count,
        'following_count': following_count
    }), 200

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_profile(user_id):
    # Check if the authenticated user is the user being updated
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    try:
      
        valid_data = user_schema.load(data, partial=True)
    except MarshmallowValidationError as err:
        
        raise ValidationError("Invalid input", errors=err.messages)
    
    # Update user fields
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'bio' in data:
        user.bio = data['bio']
    if 'location' in data:
        user.location = data['location']
    if 'expertise' in data:
        user.expertise = data['expertise']
    if 'profile_picture' in data:
        user.profile_picture = data['profile_picture']
    if 'password' in data and data['password']:
        user.password_hash = generate_password_hash(data['password'])
    
    try:
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating profile: {str(e)}'}), 500

@user_bp.route('/<int:user_id>/followers', methods=['GET'])
def get_user_followers(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    follows = UserFollow.query.filter_by(followed_id=user_id).paginate(page=page, per_page=per_page)
    
    followers = []
    for follow in follows.items:
        follower = User.query.get(follow.follower_id)
        followers.append({
            'user_id': follower.user_id,
            'username': follower.username,
            'full_name': follower.full_name,
            'profile_picture': follower.profile_picture,
            'is_expert': follower.is_expert,
            'followed_at': follow.followed_at
        })
    
    return jsonify({
        'followers': followers,
        'total': follows.total,
        'pages': follows.pages,
        'current_page': follows.page
    }), 200

@user_bp.route('/<int:user_id>/following', methods=['GET'])
def get_user_following(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    follows = UserFollow.query.filter_by(follower_id=user_id).paginate(page=page, per_page=per_page)
    
    following = []
    for follow in follows.items:
        followed = User.query.get(follow.followed_id)
        following.append({
            'user_id': followed.user_id,
            'username': followed.username,
            'full_name': followed.full_name,
            'profile_picture': followed.profile_picture,
            'is_expert': followed.is_expert,
            'followed_at': follow.followed_at
        })
    
    return jsonify({
        'following': following,
        'total': follows.total,
        'pages': follows.pages,
        'current_page': follows.page
    }), 200

@user_bp.route('/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()
    
    # Check if user is trying to follow themselves
    if current_user_id == user_id:
        return jsonify({'message': 'You cannot follow yourself'}), 400
    
    # Check if user exists
    user_to_follow = User.query.get_or_404(user_id)
    
    # Check if already following
    existing_follow = UserFollow.query.filter_by(
        follower_id=current_user_id,
        followed_id=user_id
    ).first()
    
    if existing_follow:
        return jsonify({'message': 'You are already following this user'}), 400
    
    # Create new follow relationship
    new_follow = UserFollow(
        follower_id=current_user_id,
        followed_id=user_id
    )
    
    try:
        db.session.add(new_follow)
        db.session.commit()
        return jsonify({'message': f'You are now following {user_to_follow.username}'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error following user: {str(e)}'}), 500

@user_bp.route('/<int:user_id>/follow', methods=['DELETE'])
@jwt_required()
def unfollow_user(user_id):
    current_user_id = get_jwt_identity()
    
    # Find the follow relationship
    follow = UserFollow.query.filter_by(
        follower_id=current_user_id,
        followed_id=user_id
    ).first()
    
    if not follow:
        return jsonify({'message': 'You are not following this user'}), 400
    
    try:
        db.session.delete(follow)
        db.session.commit()
        return jsonify({'message': 'User unfollowed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error unfollowing user: {str(e)}'}), 500