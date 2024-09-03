from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import logging

mongo = PyMongo()

def create_app():
    app = Flask(__name__)

    # Initialize extensions
    mongo.init_app(app)
    CORS(app)

    # Register blueprints
    from .routes import register_routes
    register_routes(app)

    return app
