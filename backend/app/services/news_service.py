from app import mongo
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NewsService:
    @staticmethod
    def get_all_news():
        """
        Fetch all news articles from the database, sorted by timestamp in descending order.

        Converts ObjectId to string for JSON serialization.

        Returns:
            list: A list of all news articles in the database.
        """
        try:
            # Fetch and sort news by timestamp in descending order (newest first)
            news_cursor = mongo.db.news.find().sort('timestamp', -1)
            
            # Convert ObjectId to string for JSON serialization
            return [{**news, '_id': str(news['_id'])} for news in news_cursor]
        except Exception as e:
            logger.error(f"Error fetching all news: {e}")
            raise e


    @staticmethod
    def get_news_article(article_id):
        """
        Fetch a specific news article by its ID.

        Args:
            article_id (str): The ObjectId of the news article.

        Returns:
            dict: The news article if found, otherwise None.
        """
        try:
            news_article = mongo.db.news.find_one({"_id": ObjectId(article_id)})
            if news_article:
                news_article['_id'] = str(news_article['_id'])  # Convert ObjectId to string
            return news_article
        except Exception as e:
            logger.error(f"Error fetching news article with ID {article_id}: {e}")
            raise e

    @staticmethod
    def add_news_article(title, content, author, is_featured=False, thumbnail=None, timestamp=None):
        """
        Add a new news article to the database.

        Args:
            title (str): The title of the article.
            content (str): The content of the article.
            author (str): The author of the article.
            is_featured (bool): Whether the article is featured.
            thumbnail (str): Optional thumbnail URL.
            timestamp (datetime): Optional timestamp. Defaults to current time.

        Returns:
            dict: The inserted article with its ID.
        """
        try:
            if timestamp is None:
                timestamp = datetime.now()  # Set the current time if no timestamp is provided

            article = {
                "title": title,
                "content": content,
                "author": author,
                "timestamp": timestamp,
                "isFeatured": is_featured,
                "thumbnail": thumbnail
            }
            result = mongo.db.news.insert_one(article)
            article['_id'] = str(result.inserted_id)
            return article
        except Exception as e:
            logger.error(f"Error adding news article: {e}")
            raise e
