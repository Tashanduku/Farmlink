# This file makes the routes directory a Python package
# It can be left empty or can import and expose route blueprints

from .auth_routes import auth_bp
from .user_routes import user_bp
from .post_routes import post_bp
from .community_routes import community_bp
from .message_routes import message_bp

# This allows importing all blueprints at once from the routes package
__all__ = ['auth_bp', 'user_bp', 'post_routes', 'community_bp', 'message_bp']