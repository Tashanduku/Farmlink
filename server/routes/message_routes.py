from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, and_
from ..models import db, Message, User

message_bp = Blueprint('messages', __name__)

@message_bp.route('', methods=['GET'])
@jwt_required()
def get_user_messages():
    current_user_id = get_jwt_identity()
    
    # Get optional query parameters
    other_user_id = request.args.get('user_id', type=int)
    community_id = request.args.get('community_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Base query
    if other_user_id:
        # Get conversation with specific user
        messages_query = Message.query.filter(
            or_(
                and_(Message.sender_id == current_user_id, Message.recipient_id == other_user_id),
                and_(Message.sender_id == other_user_id, Message.recipient_id == current_user_id)
            ),
            Message.community_id.is_(None)
        ).order_by(Message.created_at.desc())
    elif community_id:
        # Get messages from a specific community
        messages_query = Message.query.filter(
            Message.community_id == community_id
        ).order_by(Message.created_at.desc())
    else:
        # Get all user conversations (latest message from each conversation)
        # This is more complex and requires a subquery to get the latest message from each conversation
        from sqlalchemy import func, distinct
        
        # Get latest messages between current user and others
        latest_messages = db.session.query(
            func.max(Message.message_id).label('latest_message_id'),
            func.min(
                func.least(Message.sender_id, Message.recipient_id)
            ).label('user1'),
            func.max(
                func.greatest(Message.sender_id, Message.recipient_id)
            ).label('user2')
        ).filter(
            or_(
                Message.sender_id == current_user_id,
                Message.recipient_id == current_user_id
            ),
            Message.community_id.is_(None)
        ).group_by('user1', 'user2').subquery()
        
        # Get the actual messages using the IDs from the subquery
        messages_query = Message.query.join(
            latest_messages,
            Message.message_id == latest_messages.c.latest_message_id
        ).order_by(Message.created_at.desc())
    
    # Paginate results
    messages_page = messages_query.paginate(page=page, per_page=per_page)
    
    # Process messages
    messages_list = []
    for message in messages_page.items:
        sender = User.query.get(message.sender_id)
        recipient = User.query.get(message.recipient_id)
        
        # If getting all conversations, also get the other user's details
        other_user = None
        if not other_user_id and not community_id:
            other_user_id = message.sender_id if message.sender_id != current_user_id else message.recipient_id
            other_user = User.query.get(other_user_id)
        
        message_data = {
            'message_id': message.message_id,
            'content': message.content,
            'is_read': message.is_read,
            'created_at': message.created_at,
            'sender': {
                'user_id': sender.user_id,
                'username': sender.username,
                'profile_picture': sender.profile_picture
            },
            'recipient': {
                'user_id': recipient.user_id,
                'username': recipient.username,
                'profile_picture': recipient.profile_picture
            }
        }
        
        if message.community_id:
            message_data['community_id'] = message.community_id
        
        if other_user and not other_user_id and not community_id:
            message_data['conversation_with'] = {
                'user_id': other_user.user_id,
                'username': other_user.username,
                'full_name': other_user.full_name,
                'profile_picture': other_user.profile_picture
            }
        
        messages_list.append(message_data)
    
    return jsonify({
        'messages': messages_list,
        'total': messages_page.total,
        'pages': messages_page.pages,
        'current_page': messages_page.page
    }), 200

@message_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_conversation(user_id):
    current_user_id = get_jwt_identity()
    
    # Check if user exists
    User.query.get_or_404(user_id)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Get conversation with specific user
    messages_query = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user_id, Message.recipient_id == user_id),
            and_(Message.sender_id == user_id, Message.recipient_id == current_user_id)
        ),
        Message.community_id.is_(None)
    ).order_by(Message.created_at.desc())
    
    # Paginate results
    messages_page = messages_query.paginate(page=page, per_page=per_page)
    
    # Process messages
    messages_list = []
    for message in messages_page.items:
        sender = User.query.get(message.sender_id)
        
        messages_list.append({
            'message_id': message.message_id,
            'content': message.content,
            'is_read': message.is_read,
            'created_at': message.created_at,
            'is_sent_by_me': message.sender_id == current_user_id,
            'sender': {
                'user_id': sender.user_id,
                'username': sender.username,
                'profile_picture': sender.profile_picture
            }
        })
    
    # Mark unread messages as read
    try:
        unread_messages = Message.query.filter(
            Message.sender_id == user_id,
            Message.recipient_id == current_user_id,
            Message.is_read == False
        ).all()
        
        for message in unread_messages:
            message.is_read = True
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Log the error but continue with the response
        print(f"Error marking messages as read: {str(e)}")
    
    # Get other user details
    other_user = User.query.get(user_id)
    
    return jsonify({
        'conversation_with': {
            'user_id': other_user.user_id,
            'username': other_user.username,
            'full_name': other_user.full_name,
            'profile_picture': other_user.profile_picture
        },
        'messages': messages_list,
        'total': messages_page.total,
        'pages': messages_page.pages,
        'current_page': messages_page.page
    }), 200

@message_bp.route('', methods=['POST'])
@jwt_required()
def send_message():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('content'):
        return jsonify({'message': 'Message content is required'}), 400
    
    # Check recipient or community
    recipient_id = data.get('recipient_id')
    community_id = data.get('community_id')
    
    if not recipient_id and not community_id:
        return jsonify({'message': 'Either recipient_id or community_id is required'}), 400
    
    if recipient_id and community_id:
        return jsonify({'message': 'Message can only be sent to either a user or a community, not both'}), 400
    
    # If sending to a user, check if user exists
    if recipient_id:
        recipient = User.query.get(recipient_id)
        if not recipient:
            return jsonify({'message': 'Recipient not found'}), 404
    
    # Create new message
    new_message = Message(
        sender_id=current_user_id,
        recipient_id=recipient_id if recipient_id else None,
        community_id=community_id if community_id else None,
        content=data['content'],
        is_read=False
    )
    
    try:
        db.session.add(new_message)
        db.session.commit()
        
        sender = User.query.get(current_user_id)
        
        message_data = {
            'message_id': new_message.message_id,
            'content': new_message.content,
            'is_read': new_message.is_read,
            'created_at': new_message.created_at,
            'sender': {
                'user_id': sender.user_id,
                'username': sender.username,
                'profile_picture': sender.profile_picture
            }
        }
        
        if recipient_id:
            recipient = User.query.get(recipient_id)
            message_data['recipient'] = {
                'user_id': recipient.user_id,
                'username': recipient.username,
                'profile_picture': recipient.profile_picture
            }
        
        if community_id:
            message_data['community_id'] = community_id
        
        return jsonify({
            'message': 'Message sent successfully',
            'data': message_data
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error sending message: {str(e)}'}), 500

@message_bp.route('/<int:message_id>/read', methods=['PUT'])
@jwt_required()
def mark_message_read(message_id):
    current_user_id = get_jwt_identity()
    
    # Find the message
    message = Message.query.get_or_404(message_id)
    
    # Check if user is the recipient
    if message.recipient_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Check if message is already read
    if message.is_read:
        return jsonify({'message': 'Message is already marked as read'}), 400
    
    # Mark as read
    message.is_read = True
    
    try:
        db.session.commit()
        return jsonify({'message': 'Message marked as read'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error marking message as read: {str(e)}'}), 500