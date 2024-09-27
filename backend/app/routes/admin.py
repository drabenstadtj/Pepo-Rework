from flask import Blueprint, request, jsonify
from app.services.admin_service import AdminService
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Create a Blueprint for admin-related routes
bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/stocks/<symbol>/update_volatility', methods=['POST'])
def update_stock_volatility(symbol):
    """
    Update the volatility factor of a stock (admin only).
    
    Expects JSON payload with 'volatility_factor'.
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

@bp.route('/stocks/<symbol>/update_trend', methods=['POST'])
def update_stock_trend(symbol):
    """
    Update the trend direction of a stock (admin only).
    
    Expects JSON payload with 'trend_direction'.
    """
    try:
        data = request.get_json()
        trend_direction = data.get('trend_direction')

        logger.info(f"Admin request: Updating stock {symbol.upper()} with trend direction {trend_direction}")
        
        result = AdminService.update_stock_trend(symbol.upper(), trend_direction)
        
        if result:
            return jsonify({"message": "Trend direction updated successfully"}), 200
        else:
            return jsonify({"error": "Stock not found"}), 404
    except Exception as e:
        logger.error(f"Error updating stock trend direction for {symbol.upper()}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
