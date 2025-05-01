from flask import jsonify
import marshmallow

from marshmallow.exceptions import ValidationError as MarshmallowValidationError


class APIError(Exception):
    """Base class for API errors"""
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundError(APIError):
    """Resource not found"""
    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)

class ValidationError(APIError):
    """Validation error"""
    def __init__(self, message="Validation error", errors=None):
        self.errors = errors or {}
        super().__init__(message, 400)

class AuthorizationError(APIError):
    """Authorization error"""
    def __init__(self, message="Not authorized"):
        super().__init__(message, 401)

class ForbiddenError(APIError):
    """Forbidden error"""
    def __init__(self, message="Access forbidden"):
        super().__init__(message, 403)

def register_error_handlers(app):
    """Register error handlers to the Flask app"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = {
            "error": error.message,
            "status_code": error.status_code
        }
        if hasattr(error, 'errors') and error.errors:
            response["errors"] = error.errors
        return jsonify(response), error.status_code
    
    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Resource not found", "status_code": 404}), 404
    
    @app.errorhandler(500)
    def handle_server_error(error):
        return jsonify({"error": "Internal server error", "status_code": 500}), 500
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"error": "Method not allowed", "status_code": 405}), 405
    
    # Handle marshmallow validation errors
    @app.errorhandler(marshmallow.exceptions.ValidationError)
    def handle_validation_error(error):
        return jsonify({
            "error": "Validation error",
            "errors": error.messages,
            "status_code": 400
        }), 400
