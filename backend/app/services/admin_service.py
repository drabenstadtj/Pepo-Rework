from app import mongo
import logging

logger = logging.getLogger(__name__)

class AdminService:
    @staticmethod
    def update_stock_volatility(stock_symbol, volatility_factor):
        """
        Update the volatility factor of a stock (admin function).

        Args:
            stock_symbol (str): The symbol of the stock.
            volatility_factor (float): The new volatility factor.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            if volatility_factor is None:
                return False

            result = mongo.db.stocks.update_one(
                {"symbol": stock_symbol},
                {"$set": {"volatility_factor": volatility_factor}}
            )
            if result.matched_count == 0:
                logger.warning(f"Stock symbol not found: {stock_symbol}")
                return False
            
            logger.info(f"Stock {stock_symbol} updated with volatility factor {volatility_factor}")
            return True
        except Exception as e:
            logger.error(f"Error updating stock volatility for {stock_symbol}: {e}")
            raise e

    @staticmethod
    def update_stock_trend(stock_symbol, trend_direction):
        """
        Update the trend direction of a stock (admin function).

        Args:
            stock_symbol (str): The symbol of the stock.
            trend_direction (float): The new trend direction.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            if trend_direction is None:
                return False

            result = mongo.db.stocks.update_one(
                {"symbol": stock_symbol},
                {"$set": {"trend_direction": trend_direction}}
            )
            if result.matched_count == 0:
                logger.warning(f"Stock symbol not found: {stock_symbol}")
                return False
            
            logger.info(f"Stock {stock_symbol} updated with trend direction {trend_direction}")
            return True
        except Exception as e:
            logger.error(f"Error updating stock trend direction for {stock_symbol}: {e}")
            raise e
