from flask import Blueprint, jsonify, request
from app.services.shop_service import ShopService
import jwt
from functools import wraps
import os
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a Blueprint for shop-related routes
bp = Blueprint('shop', __name__, url_prefix='/shop')

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
            username = data['username']  # Assuming 'username' is stored in the token
            logger.info(f"Token successfully decoded for username: {username}")
            return f(username, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired.")
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            logger.warning("Invalid token provided.")
            return jsonify({'message': 'Token is invalid!'}), 403
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return jsonify({'message': 'Token verification failed!'}), 500

    return decorated

@bp.route('/purchase', methods=['POST'])
@token_required
def purchase_title(username):
    """
    Endpoint for purchasing a title.
    Expects JSON payload with the title level.
    """
    data = request.json
    level = data.get("level")

    if level is None:
        logger.warning("Level is missing from the request.")
        return jsonify({'message': 'Level is required!'}), 400

    result = ShopService.purchase_title(username, level)
    return jsonify(result)

@bp.route('/titles', methods=['GET'])
def get_shop_data():
    """
    Endpoint for retrieving shop data (titles and prices).
    """
    titles = ShopService.get_shop_data()
    if titles:
        return jsonify(titles), 200
    else:
        return jsonify({"message": "No titles found."}), 404
