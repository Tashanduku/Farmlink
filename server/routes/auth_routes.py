from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from ..models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # Get user data from request
    data = request.get_json()
    
    # Check if required fields are provided
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 409
    
    # Create new user
    hashed_password = generate_password_hash(data['password'])
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password,
        full_name=data.get('full_name', ''),
        bio=data.get('bio', ''),
        location=data.get('location', ''),
        expertise=data.get('expertise', ''),
        is_expert=data.get('is_expert', False)
    )
    
    # Save user to database
    try:
        db.session.add(new_user)
        db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(identity=new_user.user_id)
        refresh_token = create_refresh_token(identity=new_user.user_id)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'user_id': new_user.user_id,
                'username': new_user.username,
                'email': new_user.email,
                'full_name': new_user.full_name
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating user: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    # Get login data
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    # Find user by username
    user = User.query.filter_by(username=data['username']).first()
    
    # Check if user exists and password is correct
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    # Generate tokens
    access_token = create_access_token(identity=user.user_id)
    refresh_token = create_refresh_token(identity=user.user_id)
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name
        },
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    
    return jsonify({
        'access_token': access_token
    }), 200