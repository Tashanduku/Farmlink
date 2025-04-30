from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from server.config import Config

from server.models import db
from server.routes.auth_routes import auth_bp
from server.routes.user_routes import user_bp
from server.routes.post_routes import post_bp
from server.routes.community_routes import community_bp
from server.routes.message_routes import message_bp
from marshmallow import ValidationError
from .error_handlers import register_error_handlers

ma = Marshmallow()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(user_bp, url_prefix='/api/v1/users')
    app.register_blueprint(post_bp, url_prefix='/api/v1/posts')
    app.register_blueprint(community_bp, url_prefix='/api/v1/communities')
    app.register_blueprint(message_bp, url_prefix='/api/v1/messages')
    

    register_error_handlers(app)
    @app.route('/')
    def index():
        return "Welcome to the Farmlink API"
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)