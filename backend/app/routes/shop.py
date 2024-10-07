from flask import Blueprint, jsonify, request, current_app
from app.services.shop_service import ShopService
import jwt
from functools import wraps
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a Blueprint for shop-related routes
bp = Blueprint('shop', __name__, url_prefix='/shop')

def token_required(f):
    """
    Decorator to ensure a valid JWT token is present in the request header.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            logger.warning("Token is missing or improperly formatted.")
            return jsonify({'message': 'Token is missing or improperly formatted!'}), 403

        try:
            token = token.split()[1]
            
            # Access the SECRET_KEY inside a valid application context
            secret_key = current_app.config['SECRET_KEY']
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
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

@bp.route('/purchase', methods=['POST'])
@token_required
def purchase_title(user_id):
    """
    Endpoint for purchasing a title.
    Expects JSON payload with the title level.
    """
    data = request.json
    level = data.get("level")

    if level is None:
        logger.warning("Level is missing from the request.")
        return jsonify({'message': 'Level is required!'}), 400

    result = ShopService.purchase_title({"user_id": user_id, "level": level})

    return jsonify(result)
