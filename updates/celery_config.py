from celery import Celery
from celery.schedules import crontab

# Configure Celery to use Redis as the broker
app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

# Define the Celery Beat schedule for running tasks between 9 AM and 5 PM every 10 minutes
app.conf.beat_schedule = {
    'update-stock-prices': {
        'task': 'tasks.update_stock_prices',
        'schedule': crontab(minute='*/10', hour='9-16'),  # Every 10 minutes between 9 AM and 5 PM
    },
    'store-live-interest-data': {
        'task': 'tasks.store_live_interest_data',
        'schedule': crontab(minute='*/10', hour='9-16'),  # Every 10 minutes between 9 AM and 5 PM
    },
}

# Load task modules
app.conf.timezone = 'UTC'
