from flask import Blueprint

# Import your route modules
from .auth import bp as auth_bp
from .stocks import bp as stocks_bp
from .transactions import bp as transactions_bp
from .portfolio import bp as portfolio_bp
from .leaderboard import bp as leaderboard_bp
from .admin import bp as admin_bp
from .news import bp as news_bp
from .shop import bp as shop_bp

# Create a function to register all blueprints
def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(stocks_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(shop_bp)

    # Health check route
    @app.route('/healthcheck', methods=['GET'])
    def healthcheck():
        return {"status": "ok"}, 200
