from app import mongo
import logging
from bson import ObjectId

logger = logging.getLogger(__name__)

class ShopService:
    @staticmethod
    def purchase_title(data):
        """
        Allows a user to purchase a title.
        Expects the user_id and the level of the title to be purchased.
        Deducts the title's price from the user's balance and assigns the title to the user.
        Returns a success or failure message.
        """
        try:
            # Fetch user and title data
            user_id = ObjectId(data['user_id'])
            user = mongo.db.users.find_one({"_id": user_id})
            title = mongo.db.titles.find_one({"level": int(data['level'])})
            logger.info(f"Level: {data['level']}")

            if not user:
                logger.warning(f"User not found with ID: {data['user_id']}")
                return {"message": "User not found"}

            if not title:
                logger.warning(f"Title not found for level: {data['level']}")
                return {"message": "Title not found"}

            # Check if user has enough balance
            if user['balance'] < title['price']:
                logger.warning(f"Insufficient balance for user: {user['username']}. Balance: {user['balance']}, Title Price: {title['price']}")
                return {"message": "Insufficient balance"}

            # Deduct the price from user's balance and update their title
            new_balance = user['balance'] - title['price']
            mongo.db.users.update_one(
                {"_id": user_id}, 
                {"$set": {"balance": new_balance, "title_level": int(title['level'])}}
            )

            logger.info(f"User {user['username']} purchased title: {title['title']}. New balance: {new_balance}")
            return {"message": f"Title '{title['title']}' purchased successfully!", "new_balance": new_balance}

        except Exception as e:
            logger.error(f"Error purchasing title for user with ID {data['user_id']}: {e}")
            return {"message": "Error processing the purchase"}
    
    @staticmethod
    def get_shop_data():
        """
        Fetches all available titles and their prices from the titles collection.
        Returns a list of titles with their details.
        """
        try:
            titles = mongo.db.titles.find({}, {"_id": 0, "title": 1, "level": 1, "price": 1})  # Exclude _id field
            title_list = list(titles)  # Convert cursor to list

            logger.info("Fetched shop data successfully.")
            return title_list
        except Exception as e:
            logger.error(f"Error fetching shop data: {e}")
            return []
