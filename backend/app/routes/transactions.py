from flask import Blueprint, request, jsonify
from app.services.transaction_service import TransactionService
import jwt
from functools import wraps
import os
from flask_cors import CORS
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a Blueprint for transaction-related routes
bp = Blueprint('transactions', __name__, url_prefix='/transactions')

# Apply CORS
CORS(bp, supports_credentials=True)

# Load secret key from environment variables
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

def token_required(f):
    """
    Ensure a valid JWT token is present in the request header.
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

@bp.route('/buy', methods=['POST'])
@token_required
def buy_stock(user_id):
    """
    Process a stock purchase.
    
    Expects a JSON payload with stock details.
    Returns the result of the transaction.
    """
    try:
        data = request.get_json()
        data['user_id'] = user_id
        logger.info(f"Processing stock purchase for user_id: {user_id}, data: {data}")
        result = TransactionService.buy_stock(data)
        logger.info(f"Stock purchase completed for user_id: {user_id}")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error processing stock purchase for user_id {user_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/sell', methods=['POST'])
@token_required
def sell_stock(user_id):
    """
    Process a stock sale.
    
    Expects a JSON payload with stock details.
    Returns the result of the transaction.
    """
    try:
        data = request.get_json()
        data['user_id'] = user_id
        logger.info(f"Processing stock sale for user_id: {user_id}, data: {data}")
        result = TransactionService.sell_stock(data)
        logger.info(f"Stock sale completed for user_id: {user_id}")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error processing stock sale for user_id {user_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/', methods=['GET'])
@token_required
def get_transactions(user_id):
    """
    Fetch all transactions for the authenticated user.
    """
    try:
        logger.info(f"Fetching transactions for user_id: {user_id}")
        transactions = TransactionService.get_transactions(user_id)
        logger.info(f"Successfully fetched transactions for user_id: {user_id}")
        return jsonify(transactions), 200
    except Exception as e:
        logger.error(f"Error fetching transactions for user_id {user_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
