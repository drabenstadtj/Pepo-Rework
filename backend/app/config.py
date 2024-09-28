import os
import logging.config
from dotenv import load_dotenv

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
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }
        # ,
        # 'file': {
        #     'level': LOG_LEVEL,
        #     'class': 'logging.FileHandler',
        #     'filename': 'logs/app.log',
        #     'formatter': 'standard',
        # },
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

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    MONGO_URI = os.getenv('DATABASE_URI', 'mongodb://localhost:27017/')
    CORS_ORIGINS = '*'#os.getenv('CORS_ORIGINS', '*')
