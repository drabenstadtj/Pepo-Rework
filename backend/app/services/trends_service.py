from app import mongo
from pytrends.request import TrendReq
from datetime import datetime
import time

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
            TrendsService.pytrends.build_payload([keyword], cat=0, timeframe='now 1-H', geo='', gprop='')
            data = TrendsService.pytrends.interest_over_time()
            return data[keyword].iloc[-1] if not data.empty else 0
        except Exception as e:
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
            interest = TrendsService.get_trends_data(sector)
            stock = mongo.db.stocks.find_one({"sector": sector})
            if not stock:
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
        except ValueError as ve:
            raise ve
        except Exception as e:
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
            for sector in stock_sectors:
                TrendsService.update_stock_price(sector, multiplier)
                time.sleep(60 / len(stock_sectors))
        except Exception as e:
            raise e
