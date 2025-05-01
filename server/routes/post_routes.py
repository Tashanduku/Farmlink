from flask import Blueprint, request, jsonify, current_app
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from ..models import db, Post, PostImage, Comment, Like, User

post_bp = Blueprint('posts', __name__)

@post_bp.route('', methods=['GET'])
def get_all_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Get all posts with pagination
    posts_query = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page)
    
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
            'community_id': post.community_id,
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

@post_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Get author details
    author = User.query.get(post.user_id)
    
    # Get image URLs
    images = [{'image_id': img.image_id, 'image_url': img.image_url, 'caption': img.caption} 
              for img in post.images]
    
    # Get likes and comments count
    likes_count = Like.query.filter_by(post_id=post.post_id).count()
    comments_count = Comment.query.filter_by(post_id=post.post_id).count()
    
    # Check if current user liked the post
    current_user_id = None
    is_liked = False
    
    if 'Authorization' in request.headers:
        try:
            from flask_jwt_extended import decode_token
            token = request.headers['Authorization'].split()[1]
            current_user_id = decode_token(token)['sub']
            is_liked = Like.query.filter_by(
                post_id=post.post_id,
                user_id=current_user_id
            ).first() is not None
        except:
            pass
    
    post_data = {
        'post_id': post.post_id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at,
        'updated_at': post.updated_at,
        'community_id': post.community_id,
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
    }
    
    return jsonify(post_data), 200

@post_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Title and content are required'}), 400
    
    # Create new post
    new_post = Post(
        user_id=current_user_id,
        title=data['title'],
        content=data['content'],
        community_id=data.get('community_id')
    )
    
    try:
        db.session.add(new_post)
        db.session.flush()  # Get the post_id before committing
        
        # Add images if provided
        if 'images' in data and isinstance(data['images'], list):
            for img_data in data['images']:
                if 'image_url' in img_data:
                    new_image = PostImage(
                        post_id=new_post.post_id,
                        image_url=img_data['image_url'],
                        caption=img_data.get('caption', '')
                    )
                    db.session.add(new_image)
        
        db.session.commit()
        return jsonify({
            'message': 'Post created successfully',
            'post_id': new_post.post_id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating post: {str(e)}'}), 500

@post_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    current_user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    
    # Check if user is the author
    if post.user_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update post fields
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'community_id' in data:
        post.community_id = data['community_id']
    
    try:
        db.session.commit()
        return jsonify({'message': 'Post updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating post: {str(e)}'}), 500

@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    
    # Check if user is the author
    if post.user_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    try:
        # Delete all associated images first
        PostImage.query.filter_by(post_id=post_id).delete()
        # Delete all associated comments
        Comment.query.filter_by(post_id=post_id).delete()
        # Delete all associated likes
        Like.query.filter_by(post_id=post_id).delete()
        # Delete the post
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error deleting post: {str(e)}'}), 500

@post_bp.route('/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    current_user_id = get_jwt_identity()
    
    # Check if post exists
    post = Post.query.get_or_404(post_id)
    
    # Check if user already liked the post
    existing_like = Like.query.filter_by(
        post_id=post_id,
        user_id=current_user_id
    ).first()
    
    if existing_like:
        return jsonify({'message': 'You already liked this post'}), 400
    
    # Create new like
    new_like = Like(
        post_id=post_id,
        user_id=current_user_id
    )
    
    try:
        db.session.add(new_like)
        db.session.commit()
        
        # Get updated likes count
        likes_count = Like.query.filter_by(post_id=post_id).count()
        
        return jsonify({
            'message': 'Post liked successfully',
            'likes_count': likes_count
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error liking post: {str(e)}'}), 500

@post_bp.route('/<int:post_id>/like', methods=['DELETE'])
@jwt_required()
def unlike_post(post_id):
    current_user_id = get_jwt_identity()
    
    # Find the like
    like = Like.query.filter_by(
        post_id=post_id,
        user_id=current_user_id
    ).first()
    
    if not like:
        return jsonify({'message': 'You have not liked this post'}), 400
    
    try:
        db.session.delete(like)
        db.session.commit()
        
        # Get updated likes count
        likes_count = Like.query.filter_by(post_id=post_id).count()
        
        return jsonify({
            'message': 'Post unliked successfully',
            'likes_count': likes_count
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error unliking post: {str(e)}'}), 500

@post_bp.route('/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    # Check if post exists
    Post.query.get_or_404(post_id)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    comments_query = Comment.query.filter_by(post_id=post_id).order_by(
        Comment.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    comments_list = []
    for comment in comments_query.items:
        # Get author details
        author = User.query.get(comment.user_id)
        
        comments_list.append({
            'comment_id': comment.comment_id,
            'content': comment.content,
            'created_at': comment.created_at,
            'updated_at': comment.updated_at,
            'author': {
                'user_id': author.user_id,
                'username': author.username,
                'full_name': author.full_name,
                'profile_picture': author.profile_picture
            }
        })
    
    return jsonify({
        'comments': comments_list,
        'total': comments_query.total,
        'pages': comments_query.pages,
        'current_page': comments_query.page
    }), 200

@post_bp.route('/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    current_user_id = get_jwt_identity()
    
    # Check if post exists
    Post.query.get_or_404(post_id)
    
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('content'):
        return jsonify({'message': 'Comment content is required'}), 400
    
    # Create new comment
    new_comment = Comment(
        post_id=post_id,
        user_id=current_user_id,
        content=data['content']
    )
    
    try:
        db.session.add(new_comment)
        db.session.commit()
        
        # Get author details
        author = User.query.get(current_user_id)
        
        return jsonify({
            'message': 'Comment added successfully',
            'comment': {
                'comment_id': new_comment.comment_id,
                'content': new_comment.content,
                'created_at': new_comment.created_at,
                'author': {
                    'user_id': author.user_id,
                    'username': author.username,
                    'full_name': author.full_name,
                    'profile_picture': author.profile_picture
                }
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error adding comment: {str(e)}'}), 500
    
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@post_bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_image():
    current_user_id = get_jwt_identity()

    if 'image' not in request.files:
        return jsonify({'message': 'No image file provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'message': 'Unsupported file type'}), 400

    # Secure and save the file
    filename = secure_filename(file.filename)
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # Generate image URL (adjust if you're using a custom domain or storage)
    image_url = f"/{upload_folder}/{filename}"

    # Optionally link the image to a post
    post_id = request.form.get('post_id')
    if post_id:
        post = Post.query.get_or_404(post_id)
        if post.user_id != current_user_id:
            return jsonify({'message': 'Unauthorized to add image to this post'}), 403
        new_image = PostImage(post_id=post_id, image_url=image_url)
        db.session.add(new_image)
        db.session.commit()

    return jsonify({
        'message': 'Image uploaded successfully',
        'image_url': image_url
    }), 201