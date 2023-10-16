import requests
from werkzeug.security import check_password_hash
from p.database_manager import DatabaseManager

API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"

def get_stock_price(symbol):
    BASE_URL = "https://www.alphavantage.co/query"
    parameters = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=parameters).json()
    return float(response["Global Quote"]["05. price"])

def authenticate_user(username, password, db_manager):
    stored_password = db_manager.get_password(username)
    if stored_password and check_password_hash(stored_password[0], password):
        return True
    return False
