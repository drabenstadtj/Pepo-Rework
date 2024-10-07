import os
import json
from pymongo import MongoClient

# MongoDB connection URI (adjust as needed)
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = 'gourdstocks'  # Replace with your database name

# Initialize MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Paths to the JSON files
STOCKS_FILE = 'stocks.json'
TITLES_FILE = 'titles.json'

def load_data_from_json(file_path):
    """Load data from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def initialize_collections():
    """Initialize collections and seed data for stocks and titles."""
    
    # Create empty collections if they don't exist
    collections = ['users', 'transactions', 'stocks', 'titles']
    for collection in collections:
        if collection not in db.list_collection_names():
            db.create_collection(collection)
            print(f"Created collection: {collection}")

    # Insert initial data into 'stocks' collection
    stocks_data = load_data_from_json(STOCKS_FILE)
    if 'stocks' in db.list_collection_names() and stocks_data:
        db.stocks.insert_many(stocks_data)
        print(f"Inserted {len(stocks_data)} documents into 'stocks' collection.")

    # Insert initial data into 'titles' collection
    titles_data = load_data_from_json(TITLES_FILE)
    if 'titles' in db.list_collection_names() and titles_data:
        db.titles.insert_many(titles_data)
        print(f"Inserted {len(titles_data)} documents into 'titles' collection.")

if __name__ == "__main__":
    initialize_collections()

