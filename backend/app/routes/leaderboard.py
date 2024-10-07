from flask import Blueprint, jsonify, request
from app.services.leaderboard_service import LeaderboardService
import logging
import os

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a Blueprint for leaderboard-related routes
bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

@bp.route('', methods=['GET'])
def get_leaderboard():
    """
    Fetch the current leaderboard.
    Supports pagination using 'page' and 'limit' query parameters.
    """
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)

        logger.info(f"Fetching the leaderboard")
        leaderboard = LeaderboardService.get_leaderboard()
        
        if not leaderboard:
            logger.warning("Leaderboard data is empty")
            return jsonify({"message": "No data available"}), 404
        else:
            logger.info("Successfully fetched the leaderboard")
            return jsonify(leaderboard), 200
    except Exception as e:
        logger.error(f"Error fetching the leaderboard: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
