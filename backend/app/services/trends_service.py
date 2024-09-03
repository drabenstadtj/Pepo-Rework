from app import mongo
from pytrends.request import TrendReq
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

class TrendsService:
    pytrends = TrendReq(hl='en-US', tz=360)

    @staticmethod
    def get_trends_data(keyword):
        """
        Fetch interest data for a specific keyword using Google Trends.
        
        Args:
            keyword (str): The keyword to fetch trends data for.
        
        Returns:
            float: The latest interest value for the keyword, or 0 if no data is found.
        """
        try:
            logger.info(f"Fetching Google Trends data for keyword: {keyword}")
            TrendsService.pytrends.build_payload([keyword], cat=0, timeframe='now 1-H', geo='', gprop='')
            data = TrendsService.pytrends.interest_over_time()
            interest_value = data[keyword].iloc[-1] if not data.empty else 0
            logger.info(f"Google Trends data for '{keyword}': {interest_value}")
            return interest_value
        except Exception as e:
            logger.error(f"Error fetching trends data for keyword '{keyword}': {e}")
            raise e

    @staticmethod
    def update_stock_price(sector, multiplier):
        """
        Update the price of a stock sector based on Google Trends data.
        
        Args:
            sector (str): The stock sector to update.
            multiplier (float): The factor by which to adjust the stock price based on interest.
        """
        try:
            logger.info(f"Updating stock price for sector: {sector} with multiplier: {multiplier}")
            interest = TrendsService.get_trends_data(sector)
            stock = mongo.db.stocks.find_one({"sector": sector})
            if not stock:
                logger.warning(f"Stock sector '{sector}' not found")
                raise ValueError(f"Stock sector '{sector}' not found")

            new_price = interest * multiplier
            mongo.db.stocks.update_one(
                {'_id': stock['_id']},
                {'$set': {
                    'price': new_price,
                    'high': max(stock.get('high', new_price), new_price),
                    'low': min(stock.get('low', new_price), new_price),
                    'change': new_price - stock['price'],
                    'last_update': datetime.now()
                }}
            )
            logger.info(f"Updated stock price for sector '{sector}' to {new_price}")
        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            raise ve
        except Exception as e:
            logger.error(f"Error updating stock price for sector '{sector}': {e}")
            raise e

    @staticmethod
    def schedule_trend_updates(stock_sectors, multiplier):
        """
        Schedule periodic updates for all stock sectors based on Google Trends data.
        
        Args:
            stock_sectors (list): A list of stock sectors to update.
            multiplier (float): The factor by which to adjust the stock prices based on interest.
        """
        try:
            logger.info(f"Scheduling trend updates for stock sectors: {stock_sectors} with multiplier: {multiplier}")
            for sector in stock_sectors:
                TrendsService.update_stock_price(sector, multiplier)
                time.sleep(60 / len(stock_sectors))  # Sleep to avoid overloading
            logger.info("Completed scheduling trend updates")
        except Exception as e:
            logger.error(f"Error during scheduling trend updates: {e}")
            raise e
