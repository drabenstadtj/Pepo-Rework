from flask import Blueprint, request, jsonify, current_app
from app.services.user_service import UserService
import jwt
import datetime
from functools import wraps
import logging

# Create a Blueprint for authentication-related routes
bp = Blueprint('auth', __name__, url_prefix='/auth')
logger = logging.getLogger(__name__)

# Decorator to ensure a valid JWT token is present in the request header
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logger.warning("Token is missing from the request.")
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            token = token.split()[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['user_id']
            logger.info(f"Token successfully decoded for user_id: {user_id}")
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired.")
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            logger.warning("Invalid token provided.")
            return jsonify({'message': 'Token is invalid!'}), 403
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return jsonify({'message': 'Token verification failed!'}), 403

        return f(user_id, *args, **kwargs)

    return decorated

# Route to verify user credentials and issue a JWT token
@bp.route('/verify_credentials', methods=['POST'])
def verify_credentials():
    data = request.get_json()
    logger.info(f"Verifying credentials for username: {data.get('username')}")
    
    user = UserService.verify_credentials(data)
    if user:
        token = jwt.encode({
            'user_id': str(user['_id']),
            'isAdmin': user['isAdmin'],  # Include isAdmin in the token
            'exp': datetime.datetime.now() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        
        logger.info(f"Credentials verified for user_id: {user['_id']}. Token generated.")
        return jsonify({"message": "Credentials verified", "token": token, "isAdmin": user['isAdmin']}), 200
    else:
        logger.warning(f"Invalid credentials provided for username: {data.get('username')}")
        return jsonify({"error": "Invalid username or password"}), 401

# Route to register a new user
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    data['username'] = data['username'].strip()
    data['password'] = data['password'].strip()

    logger.info(f"Attempting to register new user with username: {data.get('username')}")
    
    result = UserService.register_user(data)
    
    if "message" in result and result["message"] == "User registered successfully":
        logger.info(f"User {data.get('username')} registered successfully.")
        return jsonify(result), 200
    elif "message" in result and result["message"] == "Duplicate user not registered":
        logger.warning(f"Username {data.get('username')} is already taken.")
        return jsonify({"error": "Username is already taken!"}), 409  # 409 Conflict
    else:
        logger.error(f"Failed to register user {data.get('username')}.")
        return jsonify({"error": "Failed to register user!"}), 500


# Route to get the user ID by username, requires a valid JWT token
@bp.route('/get_user_id', methods=['GET'])
@token_required
def get_user_id(current_user):
    username = request.args.get('username')
    logger.info(f"Fetching user ID for username: {username}")

    user_id = UserService.get_user_id(username)
    if user_id:
        logger.info(f"User ID for username {username} is {user_id}.")
        return jsonify({"_id": str(user_id)}), 200
    else:
        logger.warning(f"User {username} not found.")
        return jsonify({"error": "User not found"}), 404
