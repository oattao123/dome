from flask import Flask, render_template, request
import mysql.connector
import requests
from werkzeug.security import check_password_hash

app = Flask(__name__)

API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"

def get_stock_price(symbol):
    BASE_URL = "https://www.alphavantage.co/query"
    parameters = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }
    
    response = requests.get(BASE_URL, parameters).json()
    return float(response["Global Quote"]["05. price"])


def calculate_user_portfolio_value(username):
    connection = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="@oattao@123", 
        database="StockPortfolio"
    )
    cursor = connection.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username=%s", (username,))
    user_id = cursor.fetchone()
    if not user_id:
        return None, None

    query = "SELECT stock_name, stock_quantity FROM stocks WHERE user_id=%s"
    cursor.execute(query, (user_id[0],))

    total_value = 0.0
    for stock_name, stock_quantity in cursor.fetchall():
        stock_price = get_stock_price(stock_name)
        total_value += stock_price * stock_quantity

    cursor.close()
    connection.close()

    return user_id[0], total_value


def authenticate_user(username, password):
    connection = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="@oattao@123", 
        database="StockPortfolio"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    stored_password = cursor.fetchone()
    cursor.close()
    connection.close()

    if stored_password and check_password_hash(stored_password[0], password):
        return True
    return False


@app.route('/calculate', methods=['POST'])
def calculate():
    username = request.form['username']
    password = request.form['password']

    if not authenticate_user(username, password):
        return "Invalid username or password!", 403

    user_id, portfolio_value = calculate_user_portfolio_value(username)
    if user_id is None:
        return "Username not found!", 404
    return render_template('result.html', user_id=user_id, user=username, value=portfolio_value)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    username = request.form['username']
    password = request.form['password']

    if not authenticate_user(username, password):
        return "Invalid username or password!", 403

    user_id, portfolio_value = calculate_user_portfolio_value(username)
    if user_id is None:
        return "Username not found!", 404
    return render_template('result.html', user_id=user_id, user=username, value=portfolio_value)

if __name__ == "__main__":
    app.run(debug=True)
