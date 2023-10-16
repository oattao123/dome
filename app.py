from flask import Flask, session
from p.views import login, sign_in, calculate, add_stock, delete_stock
from p.database_manager import DatabaseManager

class StockPortfolioApp:
    API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"

    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'some_random_string'

        # Routes
        self.app.route('/')(login)
        self.app.route('/sign_in', methods=['GET', 'POST'])(sign_in)
        self.app.route('/calculate', methods=['POST'])(calculate)
        self.app.route('/add_stock', methods=['POST'])(add_stock)
        self.app.route('/delete_stock', methods=['POST'])(delete_stock)

if __name__ == "__main__":
    app_instance = StockPortfolioApp()
    app_instance.app.run(debug=True)
