from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Community, CommunityMember, User, Post

community_bp = Blueprint('communities', __name__)

@community_bp.route('', methods=['GET'])
def get_all_communities():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    communities_query = Community.query.paginate(page=page, per_page=per_page)
    
    current_user_id = None
    if 'Authorization' in request.headers:
        try:
            from flask_jwt_extended import decode_token
            token = request.headers['Authorization'].split()[1]
            current_user_id = decode_token(token)['sub']
        except:
            pass
    
    communities_list = []
    for community in communities_query.items:
        # Get creator details
        creator = User.query.get(community.creator_id)
        
        # Get membership count
        members_count = CommunityMember.query.filter_by(community_id=community.community_id).count()
        
        # Get posts count
        posts_count = Post.query.filter_by(community_id=community.community_id).count()
        
        # Check if current user is a member
        is_member = False
        if current_user_id:
            is_member = CommunityMember.query.filter_by(
                community_id=community.community_id,
                user_id=current_user_id
            ).first() is not None
        
        communities_list.append({
            'community_id': community.community_id,
            'name': community.name,
            'description': community.description,
            'community_picture': community.community_picture,
            'created_at': community.created_at,
            'creator': {
                'user_id': creator.user_id,
                'username': creator.username,
                'full_name': creator.full_name
            },
            'members_count': members_count,
            'posts_count': posts_count,
            'is_member': is_member
        })
    
    return jsonify({
        'communities': communities_list,
        'total': communities_query.total,
        'pages': communities_query.pages,
        'current_page': communities_query.page
    }), 200

@community_bp.route('/<int:community_id>', methods=['GET'])
def get_community(community_id):
    community = Community.query.get_or_404(community_id)
    
    # Get creator details
    creator = User.query.get(community.creator_id)
    
    # Get membership count
    members_count = CommunityMember.query.filter_by(community_id=community_id).count()
    
    # Get posts count
    posts_count = Post.query.filter_by(community_id=community_id).count()
    
    # Check if current user is a member
    current_user_id = None
    is_member = False
    
    if 'Authorization' in request.headers:
        try:
            from flask_jwt_extended import decode_token
            token = request.headers['Authorization'].split()[1]
            current_user_id = decode_token(token)['sub']
            is_member = CommunityMember.query.filter_by(
                community_id=community_id,
                user_id=current_user_id
            ).first() is not None
        except:
            pass
    
    community_data = {
        'community_id': community.community_id,
        'name': community.name,
        'description': community.description,
        'community_picture': community.community_picture,
        'created_at': community.created_at,
        'creator': {
            'user_id': creator.user_id,
            'username': creator.username,
            'full_name': creator.full_name
        },
        'members_count': members_count,
        'posts_count': posts_count,
        'is_member': is_member
    }
    
    return jsonify(community_data), 200

@community_bp.route('', methods=['POST'])
@jwt_required()
def create_community():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('name'):
        return jsonify({'message': 'Community name is required'}), 400
    
    # Create new community
    new_community = Community(
        name=data['name'],
        description=data.get('description', ''),
        creator_id=current_user_id,
        community_picture=data.get('community_picture', '')
    )
    
    try:
        db.session.add(new_community)
        db.session.flush()  # Get the community_id before committing
        
        # Add creator as a member
        member = CommunityMember(
            community_id=new_community.community_id,
            user_id=current_user_id
        )
        db.session.add(member)
        
        db.session.commit()
        return jsonify({
            'message': 'Community created successfully',
            'community_id': new_community.community_id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating community: {str(e)}'}), 500

@community_bp.route('/<int:community_id>', methods=['PUT'])
@jwt_required()
def update_community(community_id):
    current_user_id = get_jwt_identity()
    community = Community.query.get_or_404(community_id)
    
    # Check if user is the creator
    if community.creator_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update community fields
    if 'name' in data:
        community.name = data['name']
    if 'description' in data:
        community.description = data['description']
    if 'community_picture' in data:
        community.community_picture = data['community_picture']
    
    try:
        db.session.commit()
        return jsonify({'message': 'Community updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating community: {str(e)}'}), 500

@community_bp.route('/<int:community_id>/members', methods=['GET'])
def get_community_members(community_id):
    # Check if community exists
    Community.query.get_or_404(community_id)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    members_query = CommunityMember.query.filter_by(community_id=community_id).paginate(page=page, per_page=per_page)
    
    members_list = []
    for member in members_query.items:
        user = User.query.get(member.user_id)
        members_list.append({
            'user_id': user.user_id,
            'username': user.username,
            'full_name': user.full_name,
            'profile_picture': user.profile_picture,
            'is_expert': user.is_expert,
            'joined_at': member.joined_at
        })
    
    return jsonify({
        'members': members_list,
        'total': members_query.total,
        'pages': members_query.pages,
        'current_page': members_query.page
    }), 200

@community_bp.route('/<int:community_id>/join', methods=['POST'])
@jwt_required()
def join_community(community_id):
    current_user_id = get_jwt_identity()
    
    # Check if community exists
    Community.query.get_or_404(community_id)
    
    # Check if user is already a member
    existing_membership = CommunityMember.query.filter_by(
        community_id=community_id,
        user_id=current_user_id
    ).first()
    
    if existing_membership:
        return jsonify({'message': 'You are already a member of this community'}), 400
    
    # Create new membership
    new_membership = CommunityMember(
        community_id=community_id,
        user_id=current_user_id
    )
    
    try:
        db.session.add(new_membership)
        db.session.commit()
        return jsonify({'message': 'Successfully joined the community'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error joining community: {str(e)}'}), 500

@community_bp.route('/<int:community_id>/leave', methods=['DELETE'])
@jwt_required()
def leave_community(community_id):
    current_user_id = get_jwt_identity()
    
    # Find the membership
    membership = CommunityMember.query.filter_by(
        community_id=community_id,
        user_id=current_user_id
    ).first()
    
    if not membership:
        return jsonify({'message': 'You are not a member of this community'}), 400
    
    # Check if user is the creator of the community
    community = Community.query.get(community_id)
    if community.creator_id == current_user_id:
        return jsonify({'message': 'As the creator, you cannot leave the community'}), 400
    
    try:
        db.session.delete(membership)
        db.session.commit()
        return jsonify({'message': 'Successfully left the community'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error leaving community: {str(e)}'}), 500

@community_bp.route('/<int:community_id>/posts', methods=['GET'])
def get_community_posts(community_id):
    # Check if community exists
    Community.query.get_or_404(community_id)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts_query = Post.query.filter_by(community_id=community_id).order_by(
        Post.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    current_user_id = None
    if 'Authorization' in request.headers:
        try:
            from flask_jwt_extended import decode_token
            token = request.headers['Authorization'].split()[1]
            current_user_id = decode_token(token)['sub']
        except:
            pass
    
    posts_list = []
    for post in posts_query.items:
        # Get author details
        author = User.query.get(post.user_id)
        
        # Get image URLs
        images = [img.image_url for img in post.images]
        
        # Get likes and comments count
        from models import Like, Comment
        likes_count = Like.query.filter_by(post_id=post.post_id).count()
        comments_count = Comment.query.filter_by(post_id=post.post_id).count()
        
        # Check if current user liked the post
        is_liked = False
        if current_user_id:
            is_liked = Like.query.filter_by(
                post_id=post.post_id,
                user_id=current_user_id
            ).first() is not None
        
        posts_list.append({
            'post_id': post.post_id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'author': {
                'user_id': author.user_id,
                'username': author.username,
                'full_name': author.full_name,
                'profile_picture': author.profile_picture,
                'is_expert': author.is_expert
            },
            'images': images,
            'likes_count': likes_count,
            'comments_count': comments_count,
            'is_liked': is_liked
        })
    
    return jsonify({
        'posts': posts_list,
        'total': posts_query.total,
        'pages': posts_query.pages,
        'current_page': posts_query.page
    }), 200