import os
import logging.config
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',  # Use StreamHandler for console logging
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}

logging.config.dictConfig(logging_config)

# Get the MODE variable
MODE = os.getenv('MODE', 'development')

# Set FLASK_ENV based on MODE
if MODE == 'production':
    os.environ['FLASK_ENV'] = 'production'
else:
    os.environ['FLASK_ENV'] = 'development'

# List of required environment variables
required_env_vars = [
    'SECRET_KEY',
    'FRONTEND_URL',
    'SESSION_SECRET',
    'SIGNUP_PASSCODE',
]

# Validate required environment variables
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    for var in missing_vars:
        logging.getLogger(__name__).error(f"Error: {var} is not set in the environment variables.")
    sys.exit(1)  # Exit the application with a non-zero status


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = 'mongodb://mongo:27017/'
    CORS_ORIGINS = os.getenv('FRONTEND_URL').split(',')
    SESSION_COOKIE_SECURE = os.getenv('MODE') == 'production'  # Secure cookies in production
