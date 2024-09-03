from flask import Blueprint, jsonify, request, make_response
from app.services.leaderboard_service import LeaderboardService
from flask_cors import CORS
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a Blueprint for leaderboard-related routes
bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

# Apply CORS
CORS(bp, supports_credentials=True)

@bp.route('', methods=['GET', 'OPTIONS'])
def get_leaderboard():
    """
    Fetch the current leaderboard.
    
    Returns a JSON object with the leaderboard data.
    """
    try:
        logger.info("Fetching the current leaderboard")
        # Retrieve the leaderboard from the service
        leaderboard = LeaderboardService.get_leaderboard()
        logger.info("Successfully fetched the leaderboard")
        return jsonify(leaderboard)
    except Exception as e:
        logger.error(f"Error fetching the leaderboard: {e}")
        return jsonify({'error': str(e)}), 500
