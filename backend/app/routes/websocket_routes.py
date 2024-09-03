# app/routes/websocket_routes.py
from flask_socketio import emit
from app import socketio
import logging

logger = logging.getLogger(__name__)

@socketio.on('connect')
def handle_connect():
    logger.info("Client connected")
    emit('message', {'data': 'Connected to the stock update service'})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info("Client disconnected")

def send_stock_update(symbol, price):
    logger.info(f"Sending stock update for {symbol}: {price}")
    socketio.emit('stock_update', {'symbol': symbol, 'price': price})
