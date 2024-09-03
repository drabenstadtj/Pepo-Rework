from flask import Blueprint, request, jsonify
from app.services.transaction_service import TransactionService
import jwt
from functools import wraps
import os
from flask_cors import CORS

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
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            token = token.split()[1]  # Extract token from 'Bearer <token>' format
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403
        except Exception:
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
        result = TransactionService.buy_stock(data)
        return jsonify(result), 200
    except Exception:
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
        result = TransactionService.sell_stock(data)
        return jsonify(result), 200
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/', methods=['GET'])
@token_required
def get_transactions(user_id):
    """
    Fetch all transactions for the authenticated user.
    """
    try:
        transactions = TransactionService.get_transactions(user_id)
        return jsonify(transactions), 200
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500
