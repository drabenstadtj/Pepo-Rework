from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
import logging
from .config import Config  # Make sure to import your Config class

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    mongo.init_app(app)
    CORS(app, origins=Config.CORS_ORIGINS)

    # Initialize logger
    logger = logging.getLogger(__name__)
    logger.info("Logging is configured.")   

    # Register blueprints
    from .routes import register_routes
    register_routes(app)

    return app