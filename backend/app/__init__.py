from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_socketio import SocketIO
import logging
from .config import Config  # Make sure to import your Config class

mongo = PyMongo()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    mongo.init_app(app)
    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Initialize logger
    logger = logging.getLogger(__name__)
    logger.info("Logging is configured.")   

    # Register blueprints
    from .routes import register_routes
    register_routes(app)

    return app