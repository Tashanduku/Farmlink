from marshmallow import Schema, fields, validate, ValidationError
from flask_marshmallow import Marshmallow

ma = Marshmallow()

def initialize_schemas(app):
    ma.init_app(app)

# User schema for validation
class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.String(validate=validate.Length(min=8), load_only=True)  # Removed required=True for updates
    full_name = fields.String(validate=validate.Length(max=100))
    location = fields.String(validate=validate.Length(max=100))
    bio = fields.String(validate=validate.Length(max=500))
    expertise = fields.String(validate=validate.Length(max=100))  # Added expertise field
   
    is_expert = fields.Boolean()  # Optional, if needed for profile updates
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = ("id", "username", "email", "password", "full_name", "location", 
                  "bio", "expertise", "profile_picture", "is_expert", "created_at")
# Post schema for validation
class PostSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=5, max=100))
    content = fields.String(required=True, validate=validate.Length(min=10))
    user_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    class Meta:
        fields = ("id", "title", "content", "user_id", "created_at", "updated_at")

# Message schema for validation
class MessageSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    content = fields.String(required=True, validate=validate.Length(min=1, max=1000))
    sender_id = fields.Integer(required=True)
    recipient_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    
    class Meta:
        fields = ("id", "content", "sender_id", "recipient_id", "created_at")

# Community schema for validation
class CommunitySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=3, max=100))
    description = fields.String(validate=validate.Length(max=1000))
    created_by = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    
    class Meta:
        fields = ("id", "name", "description", "created_by", "created_at")

# Initialize schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)
community_schema = CommunitySchema()
communities_schema = CommunitySchema(many=True)