import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    MONGO_URI = os.getenv('DATABASE_URI', 'mongodb://localhost:27017/')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

