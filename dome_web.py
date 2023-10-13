from flask import Flask, render_template, request
import mysql.connector
import requests

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

def calculate_user_portfolio_value(user_id):
    connection = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="@oattao@123", 
        database="StockPortfolio"
    )
    cursor = connection.cursor()

    query = "SELECT stock_name, stock_quantity FROM Stocks WHERE user_id=%s"
    cursor.execute(query, (user_id,))

    total_value = 0.0
    for stock_name, stock_quantity in cursor.fetchall():
        stock_price = get_stock_price(stock_name)
        total_value += stock_price * stock_quantity

    cursor.close()
    connection.close()

    return total_value

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    user_id = int(request.form['user_id'])
    portfolio_value = calculate_user_portfolio_value(user_id)
    return render_template('result.html', user_id=user_id, value=portfolio_value)

if __name__ == "__main__":
    app.run(debug=True)
