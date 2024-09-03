from app import mongo
from bson import ObjectId
from .trends_service import TrendsService
from datetime import datetime
import time
import random

class StockService:
    @staticmethod
    def get_all_stocks():
        """
        Fetch all stocks from the database.

        Converts ObjectId to string for JSON serialization.

        Returns:
            list: A list of all stocks in the database.
        """
        try:
            stocks_cursor = mongo.db.stocks.find()
            return [{**stock, '_id': str(stock['_id'])} for stock in stocks_cursor]
        except Exception as e:
            raise e

    @staticmethod
    def get_stock_price(stock_symbol):
        """
        Fetch the current price of a stock by its symbol.

        Args:
            stock_symbol (str): The symbol of the stock.

        Returns:
            float: The current price of the stock if found, otherwise None.
        """
        try:
            stock = mongo.db.stocks.find_one({"symbol": stock_symbol})
            return stock['price'] if stock else None
        except Exception as e:
            raise e

    @staticmethod
    def update_stock_prices():
        """
        Update the prices of all stocks in the database.

        Simulates price changes based on random percentage changes.
        Updates the high, low, and change values of each stock.
        """
        try:
            stocks = mongo.db.stocks.find()
            for stock in stocks:
                sector = stock.get('sector')
                if sector:
                    old_price = stock['price']
                    percentage_change = random.uniform(-10, 10)
                    new_price = old_price * (1 + percentage_change / 100.0)
                    new_high = max(stock.get('high', new_price), new_price)
                    new_low = min(stock.get('low', new_price), new_price)
                    price_change = new_price - old_price

                    mongo.db.stocks.update_one(
                        {'_id': stock['_id']},
                        {'$set': {
                            'price': new_price,
                            'high': new_high,
                            'low': new_low,
                            'change': price_change,
                            'last_update': datetime.now()
                        }}
                    )
                    time.sleep(5)
        except Exception as e:
            raise e

    @staticmethod
    def update_stock_price(stock_symbol, quantity, is_buying):
        """
        Update the price of a stock based on buying or selling quantity.

        Args:
            stock_symbol (str): The symbol of the stock.
            quantity (int): The quantity of stock being bought or sold.
            is_buying (bool): True if buying, False if selling.

        Returns:
            float: The new price of the stock if successful, otherwise an error message.
        """
        try:
            stock = mongo.db.stocks.find_one({"symbol": stock_symbol})
            if not stock:
                return {"error": f"Stock '{stock_symbol}' not found"}

            price_change = 0.1 * quantity  # Adjust this factor as needed
            new_price = stock['price'] + price_change if is_buying else stock['price'] - price_change

            old_price = stock['price']
            new_high = max(stock.get('high', new_price), new_price)
            new_low = min(stock.get('low', new_price), new_price)
            price_change = new_price - old_price

            result = mongo.db.stocks.update_one(
                {'_id': stock['_id']},
                {'$set': {
                    'price': new_price,
                    'high': new_high,
                    'low': new_low,
                    'change': price_change,
                    'last_update': datetime.now()
                }}
            )

            if result.matched_count == 0:
                return {"error": f"Failed to update stock '{stock_symbol}' in the database"}

            return new_price

        except Exception as e:
            return {"error": "An unexpected error occurred"}
