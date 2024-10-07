from flask import Blueprint, jsonify, request
from app.services.user_service import UserService
import jwt
from functools import wraps
import os
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a Blueprint for portfolio-related routes
bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

# Load environment variables
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

def token_required(f):
    """
    Decorator to ensure a valid JWT token is present in the request header.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logger.warning("Token is missing from the request.")
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            token = token.split()[1]  # Extract token from 'Bearer <token>' format
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
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

@bp.route('/stocks', methods=['GET'])
@token_required
def get_portfolio(user_id):
    """
    Fetch the user's portfolio.
    
    Expects a valid JWT token.
    Returns the user's portfolio if the user is found.
    """
    try:
        logger.info(f"Fetching portfolio for user_id: {user_id}")
        portfolio = UserService.get_portfolio(user_id)
        logger.info(f"Successfully fetched portfolio for user_id: {user_id}")
        return jsonify(portfolio), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(f"Error fetching portfolio for user_id {user_id}: {e}")
        return jsonify({'error': str(e)}), 500, {'Content-Type': 'application/json'}

@bp.route('/balance', methods=['GET'])
@token_required
def get_balance(user_id):
    """
    Fetch the user's balance.
    
    Expects a valid JWT token.
    Returns the user's balance if the user is found.
    """
    try:
        logger.info(f"Fetching balance for user_id: {user_id}")
        balance = UserService.get_balance(user_id)
        logger.info(f"Successfully fetched balance for user_id: {user_id}")
        return jsonify(balance), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(f"Error fetching balance for user_id {user_id}: {e}")
        return jsonify({'error': str(e)}), 500, {'Content-Type': 'application/json'}
    
@bp.route('/title', methods=['GET'])
@token_required
def get_title(user_id):
    """
    Fetch the user's title.

    Expects a valid JWT token.
    Returns the user's current title if found, including the title level and name.
    If the title_level is -1, it returns "none" as the title name.
    """
    try:
        logger.info(f"Fetching title for user_id: {user_id}")
        # Get the user's title level and name
        title_data = UserService.get_title(user_id)
        
        if title_data:
            logger.info(f"Successfully fetched title for user_id: {user_id}")
            # Return the title information with level and name
            return jsonify({
                "level": title_data['level'],
                "name": title_data['name']
            }), 200, {'Content-Type': 'application/json'}
        else:
            logger.warning(f"Title not found for user_id: {user_id}")
            return jsonify({"message": "Title not found"}), 404
    except Exception as e:
        logger.error(f"Error fetching title for user_id {user_id}: {e}")
        return jsonify({'error': str(e)}), 500, {'Content-Type': 'application/json'}



@bp.route('/assets_value', methods=['GET'])
@token_required
def get_assets_value(user_id):
    """
    Fetch the user's assets value.
    
    Expects a valid JWT token.
    Returns the user's assets value if the user is found.
    """
    try:
        logger.info(f"Fetching assets value for user_id: {user_id}")
        assets_value = UserService.get_assets_value(user_id)
        logger.info(f"Successfully fetched assets value for user_id: {user_id}")
        return jsonify(assets_value), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(f"Error fetching assets value for user_id {user_id}: {e}")
        return jsonify({'error': str(e)}), 500, {'Content-Type': 'application/json'}
