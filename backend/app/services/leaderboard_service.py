from app import mongo
from .stock_service import StockService
from .user_service import UserService
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
                
                # Calculate invested assets and net worth
                invested_assets = sum(
                    stock['quantity'] * StockService.get_stock_price(stock['stock_symbol'])
                    for stock in user['portfolio']
                )
                net_worth = user['balance'] + invested_assets

                # Retrieve the user's title and level
                title_data = UserService.get_title(user['_id'])  # This will return {"level": ..., "name": ...}
                title_name = title_data['name']
                title_level = title_data['level']

                # Construct the image URL for the title
                if title_level != -1:  # Ensure the user has a valid title level
                    title_image_url = f"/images/Level{title_level}.png"
                else:
                    title_image_url = None  # No title image for users with level -1

                # Append user data to the leaderboard
                leaderboard.append({
                    "username": user['username'],
                    "liquidAssets": user['balance'],
                    "investedAssets": invested_assets,
                    "netWorth": net_worth,
                    "title": title_name,  # Add title name
                    "title_image": title_image_url  # Add title image URL
                })

            # Sort leaderboard by net worth in descending order
            leaderboard.sort(key=lambda x: x['netWorth'], reverse=True)
            logger.info("Leaderboard calculated successfully.")
            return leaderboard

        except Exception as e:
            logger.error(f"Error fetching leaderboard: {e}")
            return []
