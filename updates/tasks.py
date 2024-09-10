from celery_config import app
from pytrends.request import TrendReq
import pymongo
from datetime import datetime, timedelta
import time
import random

# Setup MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['gourdstocks']
trends_collection = db['trends']
stocks_collection = db['stocks']

# Setup Pytrends
pytrends = TrendReq(hl='en-US', tz=360)


@app.task
def fetch_live_interest_data(sectors):
    try:
        pytrends.build_payload(sectors, cat=0, timeframe='now 1-H')
        interest_over_time_df = pytrends.interest_over_time()
        return interest_over_time_df
    except Exception as e:
        print(f"Error fetching data for {sectors}: {e}")
    return None


@app.task
def store_live_interest_data():
    # Get all unique sectors from the stocks collection
    sectors = stocks_collection.distinct('sector')
    
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    
    while datetime.now() < end_time and sectors:
        batch = sectors[:5]  # Take the first 5 sectors
        interest_data = fetch_live_interest_data(batch)
        if interest_data is not None:
            for sector in batch:
                if sector in interest_data.columns:
                    live_interest = int(interest_data[sector].iloc[-1])  # Convert to native Python int
                    trends_collection.update_one(
                        {'sector': sector},
                        {'$set': {'live_interest': live_interest, 'timestamp': datetime.now()}},
                        upsert=True
                    )
                    print(f'Retrieved live data for {sector}')
                else:
                    print(f'No live data for {sector}')
        else:
            print(f'Failed to fetch data for batch: {batch}')
        
        # Remove the processed sectors from the list
        sectors = sectors[5:]
        time.sleep(60)  # Wait for 1 minute between requests to avoid rate limits


@app.task
def get_live_interest_data(sector):
    trend_data = trends_collection.find_one({'sector': sector})
    if trend_data:
        return trend_data['live_interest']
    return 0


@app.task
def update_stock_prices():
    stocks = list(stocks_collection.find())
    for stock in stocks:
        sector_interest = get_live_interest_data(stock['sector'])
        
        # Base price change based on sector interest
        base_price_change = sector_interest * 0.01  # Adjust the multiplier as needed

        # Add random factor to price change
        random_factor = random.uniform(-0.05, 0.05)  # Random factor between -5% and 5%
        price_change = base_price_change + (stock['price'] * random_factor)

        # Calculate new price
        new_price = stock['price'] + price_change

        # Calculate the change as the new price minus the old price
        if not new_price == stock['price']:
            change = new_price - stock['price']
        else:
            change = stock['change']

        # Update the stock price and other relevant fields
        stocks_collection.update_one(
            {'_id': stock['_id']},
            {
                '$set': {
                    'price': new_price,
                    'last_update': datetime.now(),
                    'change': change,
                    'low': min(stock['low'], new_price),
                    'high': max(stock['high'], new_price)
                }
            }
        )
    print("Stock prices updated.")
