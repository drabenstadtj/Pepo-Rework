from app import mongo
from bson import ObjectId
from .stock_service import StockService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TransactionService:
    @staticmethod
    def buy_stock(data):
        """
        Buy a stock.
        
        Expects data to contain 'user_id', 'stock_symbol', and 'quantity'.
        Fetches the current stock price, updates user's portfolio and balance,
        and logs the transaction in the transactions collection.
        
        Args:
            data (dict): Dictionary containing 'user_id', 'stock_symbol', and 'quantity'.
        
        Returns:
            dict: A success message if the purchase is successful, or an error message otherwise.
        """
        user_id = ObjectId(data['user_id'])
        stock_symbol = data['stock_symbol'].upper()
        quantity = data['quantity']

        try:
            logger.info(f"Attempting to buy stock {stock_symbol} for user {user_id} with quantity {quantity}")
            price = StockService.get_stock_price(stock_symbol)
            if price is None:
                logger.warning(f"Stock {stock_symbol} not found")
                return {"message": "Stock not found"}

            user = mongo.db.users.find_one({"_id": user_id})
            if user and user['balance'] >= (total_price := price * quantity):
                portfolio = user.get('portfolio', [])
                stock_exists = False

                for stock in portfolio:
                    if stock['stock_symbol'] == stock_symbol:
                        stock['quantity'] += quantity
                        stock_exists = True
                        break

                if not stock_exists:
                    portfolio.append({"stock_symbol": stock_symbol, "quantity": quantity})

                mongo.db.users.update_one(
                    {"_id": user_id},
                    {"$set": {"balance": user['balance'] - total_price, "portfolio": portfolio}}
                )

                transaction = {
                    "user_id": user_id,
                    "stock_symbol": stock_symbol,
                    "quantity": quantity,
                    "price": price,
                    "total_price": total_price,
                    "type": "buy",
                    "date": datetime.now()
                }
                mongo.db.transactions.insert_one(transaction)

                logger.info(f"Stock {stock_symbol} purchased successfully for user {user_id}")

                StockService.update_stock_price(stock_symbol, quantity, is_buying=True)
                return {"message": "Stock purchased successfully"}
            logger.warning(f"User {user_id} has insufficient balance or user not found")
            return {"message": "Insufficient balance" if user else "User not found"}
        except Exception as e:
            logger.error(f"Error processing stock purchase for user {user_id}: {e}")
            return {"message": "Internal Server Error"}

    @staticmethod
    def sell_stock(data):
        """
        Sell a stock.
        
        Expects data to contain 'user_id', 'stock_symbol', and 'quantity'.
        Fetches the current stock price, updates user's portfolio and balance,
        and logs the transaction in the transactions collection.
        
        Args:
            data (dict): Dictionary containing 'user_id', 'stock_symbol', and 'quantity'.
        
        Returns:
            dict: A success message if the sale is successful, or an error message otherwise.
        """
        user_id = ObjectId(data['user_id'])
        stock_symbol = data['stock_symbol'].upper()
        quantity = data['quantity']

        try:
            logger.info(f"Attempting to sell stock {stock_symbol} for user {user_id} with quantity {quantity}")
            price = StockService.get_stock_price(stock_symbol)
            if price is None:
                logger.warning(f"Stock {stock_symbol} not found")
                return {"message": "Stock not found"}

            user = mongo.db.users.find_one({"_id": user_id})
            if user:
                portfolio = user.get('portfolio', [])
                for stock in portfolio:
                    if stock['stock_symbol'] == stock_symbol:
                        if stock['quantity'] >= quantity:
                            stock['quantity'] -= quantity
                            if stock['quantity'] == 0:
                                portfolio.remove(stock)
                            break
                else:
                    logger.warning(f"User {user_id} has insufficient stock quantity of {stock_symbol} to sell")
                    return {"message": "Insufficient stock quantity"}

                new_balance = user['balance'] + price * quantity
                mongo.db.users.update_one(
                    {"_id": user_id},
                    {"$set": {"balance": new_balance, "portfolio": portfolio}}
                )

                transaction = {
                    "user_id": user_id,
                    "stock_symbol": stock_symbol,
                    "quantity": quantity,
                    "price": price,
                    "total_price": price * quantity,
                    "type": "sell",
                    "date": datetime.now()
                }
                mongo.db.transactions.insert_one(transaction)

                logger.info(f"Stock {stock_symbol} sold successfully for user {user_id}")

                StockService.update_stock_price(stock_symbol, quantity, is_buying=False)
                return {"message": "Stock sold successfully"}
            logger.warning(f"User {user_id} not found")
            return {"message": "User not found"}
        except Exception as e:
            logger.error(f"Error processing stock sale for user {user_id}: {e}")
            return {"message": "Internal Server Error"}

    @staticmethod
    def get_transactions(user_id=None):
        """
        Fetch transactions.
        
        Optionally expects 'user_id' to filter transactions for a specific user.
        Converts ObjectId and datetime to string for JSON serialization.
        
        Args:
            user_id (str, optional): The ID of the user to filter transactions for.
        
        Returns:
            list: A list of transactions.
        """
        try:
            logger.info(f"Fetching transactions for user {user_id}" if user_id else "Fetching all transactions")
            query = {"user_id": ObjectId(user_id)} if user_id else {}
            transactions = mongo.db.transactions.find(query)
            result = [
                {
                    **transaction,
                    '_id': str(transaction['_id']),
                    'user_id': str(transaction['user_id']),
                    'date': transaction['date'].isoformat()
                }
                for transaction in transactions
            ]
            logger.info(f"Successfully fetched transactions for user {user_id}" if user_id else "Successfully fetched all transactions")
            return result
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            return {"message": "Internal Server Error"}
