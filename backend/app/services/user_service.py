from app import mongo
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from .stock_service import StockService
import logging

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    def register_user(data):
        """
        Register a new user.
        Expects data to contain 'username' and 'password'.
        Initializes user balance to 10000 and an empty portfolio.
        Stores user information in the users collection.
        Returns a success message upon successful registration.
        """

        if mongo.db.users.find_one({"username": data['username']}):
            logger.info(f"Duplicate user not registered: {data['username']}")
            return {"message": "Duplicate user not registered"}

        user = {
            "username": data['username'],
            "password": generate_password_hash(data['password']),
            "balance": 10000,
            "portfolio": [],
            "isAdmin": False
        }
        try:
            logger.info(f"Registering new user: {data['username']}")
            mongo.db.users.insert_one(user)
            logger.info(f"User {data['username']} registered successfully")
            return {"message": "User registered successfully"}
        except Exception as e:
            logger.error(f"Error registering user {data['username']}: {e}")
            return {"message": "Error registering user"}

    @staticmethod
    def get_user_id(username):
        """
        Fetch the user ID by username.
        Expects the 'username' as input.
        Returns the user ID if found, otherwise returns None.
        """
        try:
            logger.info(f"Fetching user ID for username: {username}")
            user = mongo.db.users.find_one({"username": username}, {"_id": 1})
            if user:
                logger.info(f"Found user ID for username: {username}")
                return user['_id']
            logger.warning(f"User ID not found for username: {username}")
            return None
        except Exception as e:
            logger.error(f"Error fetching user ID for username {username}: {e}")
            return None

    @staticmethod
    def verify_credentials(data):
        """
        Verify user credentials.
        Expects data to contain 'username' and 'password'.
        Returns the user object with the isAdmin field if credentials are correct.
        """
        try:
            logger.info(f"Verifying credentials for username: {data['username']}")
            user = mongo.db.users.find_one({"username": data['username']})
            if user and check_password_hash(user['password'], data['password']):
                logger.info(f"Credentials verified for user: {data['username']}")
                # Ensure that if the isAdmin field is missing, it defaults to False
                user['isAdmin'] = user.get('isAdmin', False)
                return user
            logger.warning(f"Invalid credentials for username: {data['username']}")
            return None
        except Exception as e:
            logger.error(f"Error verifying credentials for username {data['username']}: {e}")
            return None


    @staticmethod
    def get_user_by_id(user_id):
        """
        Fetch a user by user ID.
        Expects the 'user_id' as input.
        Returns the user document if found, otherwise returns None.
        """
        try:
            logger.info(f"Fetching user by ID: {user_id}")
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                logger.info(f"User found by ID: {user_id}")
                return user
            logger.warning(f"User not found by ID: {user_id}")
            return None
        except Exception as e:
            logger.error(f"Error fetching user by ID {user_id}: {e}")
            return None

    @staticmethod
    def get_portfolio(user_id):
        """
        Fetch the user's portfolio by user ID.
        Expects the 'user_id' as input.
        Converts user_id to ObjectId.
        Returns the user's portfolio if the user is found, otherwise returns an empty list.
        """
        try:
            logger.info(f"Fetching portfolio for user ID: {user_id}")
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"portfolio": 1})
            if user and 'portfolio' in user:
                portfolio = user['portfolio']
                for stock in portfolio:
                    stock['price'] = StockService.get_stock_price(stock['stock_symbol'])
                logger.info(f"Portfolio fetched for user ID: {user_id}")
                return portfolio
            logger.warning(f"No portfolio found for user ID: {user_id}")
            return []
        except Exception as e:
            logger.error(f"Error fetching portfolio for user ID {user_id}: {e}")
            return []

    @staticmethod
    def get_balance(user_id):
        """
        Fetch the user's balance by user ID.
        Expects the 'user_id' as input.
        Converts user_id to ObjectId.
        Returns the user's balance if the user is found, otherwise returns an empty list.
        """
        try:
            logger.info(f"Fetching balance for user ID: {user_id}")
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"balance": 1})
            if user and 'balance' in user:
                logger.info(f"Balance fetched for user ID: {user_id}")
                return user['balance']
            logger.warning(f"No balance found for user ID: {user_id}")
            return []
        except Exception as e:
            logger.error(f"Error fetching balance for user ID {user_id}: {e}")
            return []

    @staticmethod
    def get_assets_value(user_id):
        """
        Fetch the user's total assets value by user ID.
        Expects the 'user_id' as input.
        Converts user_id to ObjectId.
        Returns the total value of the user's assets if the user is found, otherwise returns 0.
        """
        try:
            logger.info(f"Fetching assets value for user ID: {user_id}")
            assets_value = 0
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"portfolio": 1})
            if user and 'portfolio' in user:
                for stock in user['portfolio']:
                    price = StockService.get_stock_price(stock['stock_symbol'])
                    if price:
                        assets_value += stock['quantity'] * price
                logger.info(f"Assets value calculated for user ID: {user_id}")
            else:
                logger.warning(f"No portfolio found for user ID: {user_id}")
            return assets_value
        except Exception as e:
            logger.error(f"Error fetching assets value for user ID {user_id}: {e}")
            return 0
