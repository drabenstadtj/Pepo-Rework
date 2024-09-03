from flask import Blueprint, jsonify
from app.services.stock_service import StockService
from flask_cors import CORS

# Create a Blueprint for stock-related routes
bp = Blueprint('stocks', __name__, url_prefix='/stocks')

# Apply CORS
CORS(bp, supports_credentials=True)

@bp.route('/', methods=['GET'])
def get_stocks():
    """
    Fetch all stocks.
    
    Returns a list of all stocks in the database.
    """
    try:
        stocks = StockService.get_all_stocks()
        return jsonify(stocks), 200
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    """
    Get the current price of a stock.
    
    Expects the stock symbol as a URL parameter.
    Returns the current stock price if found, otherwise returns a 404 Not Found.
    """
    try:
        price = StockService.get_stock_price(symbol.upper())
        if price is not None:
            return jsonify({"symbol": symbol.upper(), "price": price}), 200
        else:
            return jsonify({"error": "Stock not found"}), 404
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500
