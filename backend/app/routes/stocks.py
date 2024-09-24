from flask import Blueprint, jsonify
from app.services.stock_service import StockService
from flask_cors import CORS
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a Blueprint for stock-related routes
bp = Blueprint('stocks', __name__, url_prefix='/stocks')

# Apply CORS
CORS(bp, supports_credentials=True)

@bp.route('/list', methods=['GET'])
def get_stocks():
    """
    Fetch all stocks.

    Returns a list of all stocks in the database.
    """
    try:
        logger.info("Fetching all stocks from the database")
        # Call the StockService to fetch all stocks
        stocks = StockService.get_all_stocks()

        if stocks:
            logger.info(f"Successfully fetched {len(stocks)} stocks from the database")
            return jsonify(stocks), 200
        else:
            logger.warning("No stocks found in the database")
            return jsonify({"message": "No stocks found"}), 404
    except Exception as e:
        logger.error(f"Error fetching stocks: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    """
    Get the current price of a stock.
    
    Expects the stock symbol as a URL parameter.
    Returns the current stock price if found, otherwise returns a 404 Not Found.
    """
    try:
        logger.info(f"Fetching price for stock symbol: {symbol.upper()}")
        price = StockService.get_stock_price(symbol.upper())
        if price is not None:
            logger.info(f"Successfully fetched price for stock symbol: {symbol.upper()}")
            return jsonify({"symbol": symbol.upper(), "price": price}), 200
        else:
            logger.warning(f"Stock symbol not found: {symbol.upper()}")
            return jsonify({"error": "Stock not found"}), 404
    except Exception as e:
        logger.error(f"Error fetching stock price for symbol {symbol.upper()}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
