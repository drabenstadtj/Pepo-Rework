from app import mongo
import logging
from bson import ObjectId

logger = logging.getLogger(__name__)

class ShopService:
    @staticmethod
    def purchase_title(username, level):
        """
        Allows a user to purchase a title.
        Expects the username of the user and the title_id to be purchased.
        Deducts the title's price from the user's balance and assigns the title to the user.
        Returns a success or failure message.
        """
        try:
            # Fetch user and title data
            user = mongo.db.users.find_one({"username": username})
            title = mongo.db.titles.find_one({"level": level})

            if not user:
                logger.warning(f"User not found: {username}")
                return {"message": "User not found"}

            if not title:
                logger.warning(f"Title not found: {title_id}")
                return {"message": "Title not found"}

            # Check if user has enough balance
            if user['balance'] < title['price']:
                logger.warning(f"Insufficient balance for user: {username}. Balance: {user['balance']}, Title Price: {title['price']}")
                return {"message": "Insufficient balance"}

            # Deduct the price from user's balance
            new_balance = user['balance'] - title['price']
            mongo.db.users.update_one({"username": username}, {"$set": {"balance": new_balance, "title": title['title']}})

            logger.info(f"User {username} purchased title: {title['title']}. New balance: {new_balance}")
            return {"message": f"Title '{title['title']}' purchased successfully!", "new_balance": new_balance}

        except Exception as e:
            logger.error(f"Error purchasing title for user {username}: {e}")
            return {"message": "Error processing the purchase"}
    
    @staticmethod
    def get_shop_data():
        """
        Fetches all available titles and their prices from the titles collection.
        Returns a list of titles with their details.
        """
        try:
            titles = mongo.db.titles.find({}, {"_id": 0, "title": 1, "level": 1, "price": 1})  # Exclude _id field
            title_list = []
            for title in titles:
                title_list.append(title)

            logger.info("Fetched shop data successfully.")
            return title_list
        except Exception as e:
            logger.error(f"Error fetching shop data: {e}")
            return []
