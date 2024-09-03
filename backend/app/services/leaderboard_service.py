from app import mongo
from .stock_service import StockService

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
            users_cursor = mongo.db.users.find()
            leaderboard = [
                {
                    'username': user['username'],
                    'title': 'Gourd Lord',  # Example title, customize as needed
                    'liquidAssets': user['balance'],
                    'investedAssets': sum(
                        stock['quantity'] * StockService.get_stock_price(stock['stock_symbol'])
                        for stock in user['portfolio']
                    ),
                    'netWorth': user['balance'] + sum(
                        stock['quantity'] * StockService.get_stock_price(stock['stock_symbol'])
                        for stock in user['portfolio']
                    ),
                }
                for user in users_cursor
            ]

            leaderboard.sort(key=lambda x: x['netWorth'], reverse=True)
            return leaderboard
        except Exception as e:
            raise e
