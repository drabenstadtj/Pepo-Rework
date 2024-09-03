from flask import Blueprint, request, jsonify, current_app
from app.services.user_service import UserService
import jwt
import datetime
from functools import wraps

# Create a Blueprint for authentication-related routes
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Decorator to ensure a valid JWT token is present in the request header
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Retrieve the token from the Authorization header
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Extract the token by splitting the 'Bearer <token>' format
            token = token.split()[1]
            # Decode the token using the application's secret key
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            # Extract the user ID from the decoded token
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            # Handle invalid token
            return jsonify({'message': 'Token is invalid!'}), 403
        except Exception:
            # Handle any other token verification errors
            return jsonify({'message': 'Token verification failed!'}), 403

        # If the token is valid, proceed with the request and pass the user_id to the wrapped function
        return f(user_id, *args, **kwargs)

    return decorated

# Route to verify user credentials and issue a JWT token
@bp.route('/verify_credentials', methods=['POST'])
def verify_credentials():
    # Get the JSON data from the request body
    data = request.get_json()
    # Verify the user credentials using the UserService
    user_id = UserService.verify_credentials(data)
    if user_id:
        # If credentials are valid, generate a JWT token valid for 24 hours
        token = jwt.encode({
            'user_id': str(user_id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        # Return the generated token in the response
        return jsonify({"message": "Credentials verified", "token": token}), 200
    else:
        # Return an error message if credentials are invalid
        return jsonify({"error": "Invalid username or password"}), 401

# Route to register a new user
@bp.route('/register', methods=['POST'])
def register():
    # Get the JSON data from the request body
    data = request.get_json()
    # Register the new user using the UserService and return the result
    result = UserService.register_user(data)
    return jsonify(result)

# Route to get the user ID by username, requires a valid JWT token
@bp.route('/get_user_id', methods=['GET'])
@token_required
def get_user_id(current_user):
    # Get the username from the request query parameters
    username = request.args.get('username')
    # Retrieve the user ID associated with the given username
    user_id = UserService.get_user_id(username)
    if user_id:
        # Return the user ID if found
        return jsonify({"_id": str(user_id)}), 200
    else:
        # Return an error message if the user is not found
        return jsonify({"error": "User not found"}), 404
