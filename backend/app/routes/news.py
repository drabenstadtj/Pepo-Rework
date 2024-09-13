from flask import Blueprint, jsonify, request
from app.services.news_service import NewsService
from flask_cors import CORS
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a Blueprint for news-related routes
bp = Blueprint('news', __name__, url_prefix='/news')

# Apply CORS
CORS(bp, supports_credentials=True)

@bp.route('/', methods=['GET'])
def get_all_news():
    """
    Fetch all news articles.
    
    Returns a list of all news articles in the database.
    """
    try:
        logger.info("Fetching all news articles from the database")
        news_articles = NewsService.get_all_news()
        logger.info(f"Successfully fetched {len(news_articles)} news articles")
        return jsonify(news_articles), 200
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/<article_id>', methods=['GET'])
def get_news_article(article_id):
    """
    Get a specific news article by its ID.
    
    Expects the article ID as a URL parameter.
    Returns the news article if found, otherwise returns a 404 Not Found.
    """
    try:
        logger.info(f"Fetching news article with ID: {article_id}")
        article = NewsService.get_news_article(article_id)
        if article:
            logger.info(f"Successfully fetched news article with ID: {article_id}")
            return jsonify(article), 200
        else:
            logger.warning(f"News article not found with ID: {article_id}")
            return jsonify({"error": "Article not found"}), 404
    except Exception as e:
        logger.error(f"Error fetching news article with ID {article_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/', methods=['POST'])
def add_news_article():
    """
    Add a new news article.
    
    Expects JSON data with 'title', 'content', and 'author'.
    Optionally, 'isFeatured' and 'thumbnail' can be included.
    """
    try:
        data = request.json
        title = data.get('title')
        content = data.get('content')
        author = data.get('author')
        is_featured = data.get('isFeatured', False)
        thumbnail = data.get('thumbnail', None)

        if not title or not content or not author:
            logger.warning("Missing required fields for adding news article")
            return jsonify({"error": "Missing required fields"}), 400

        logger.info(f"Adding new news article: {title}")
        new_article = NewsService.add_news_article(title, content, author, is_featured, thumbnail)
        return jsonify(new_article), 201
    except Exception as e:
        logger.error(f"Error adding news article: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
