from app import mongo
from .stock_service import StockService
import logging

logger = logging.getLogger(__name__)

class LeaderboardService:
    @staticmethod
    def get_leaderboard():
        """
        Fetch the leaderboard data.

        Retrieves user data from the database, calculates the net worth for each user,
        and sorts the users by their net worth in descending order.

        Returns:
            list: A list of dictionaries containing the leaderboard data.
        """
        try:
            logger.info("Fetching users from the database for leaderboard calculation.")
            users_cursor = mongo.db.users.find()

            leaderboard = []
            for user in users_cursor:
                logger.info(f"Calculating net worth for user: {user['username']}")
                invested_assets = sum(
                    stock['quantity'] * StockService.get_stock_price(stock['stock_symbol'])
                    for stock in user['portfolio']
                )
                net_worth = user['balance'] + invested_assets

                leaderboard.append({
                    'username': user['username'],
                    'title': 'Gourd Lord',  # Example title, customize as needed
                    'liquidAssets': user['balance'],
                    'investedAssets': invested_assets,
                    'netWorth': net_worth,
                })

            leaderboard.sort(key=lambda x: x['netWorth'], reverse=True)
            logger.info("Leaderboard calculated and sorted successfully.")
            return leaderboard
        except Exception as e:
            logger.error(f"Error occurred while calculating the leaderboard: {e}")
            raise e
