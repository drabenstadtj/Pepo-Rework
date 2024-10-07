from flask import Blueprint, request, jsonify
from app.services.admin_service import AdminService
from app.services.user_service import UserService
import logging
from functools import wraps

# Initialize logger
logger = logging.getLogger(__name__)

# Create a Blueprint for admin-related routes
bp = Blueprint('admin', __name__, url_prefix='/admin')

def is_admin_required(f):
    @wraps(f)
    def decorated(user_id, *args, **kwargs):
        user = UserService.get_user_by_id(user_id)
        if not user or not user.get('isAdmin', False):
            logger.warning(f"Unauthorized access attempt by user {user_id}")
            return jsonify({'error': 'Unauthorized access'}), 403
        return f(user_id, *args, **kwargs)
    return decorated

@bp.route('/stocks/<symbol>/update_volatility', methods=['POST'])
@is_admin_required
def update_stock_volatility(user_id, symbol):
    """
    Update the volatility factor of a stock (admin only).
    """
    try:
        data = request.get_json()
        volatility_factor = data.get('volatility_factor')

        logger.info(f"Admin request: Updating stock {symbol.upper()} with volatility {volatility_factor}")
        result = AdminService.update_stock_volatility(symbol.upper(), volatility_factor)
        
        if result:
            return jsonify({"message": "Volatility updated successfully"}), 200
        else:
            return jsonify({"error": "Stock not found"}), 404
    except Exception as e:
        logger.error(f"Error updating stock volatility for {symbol.upper()}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
