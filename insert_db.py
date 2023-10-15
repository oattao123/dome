import mysql.connector
from werkzeug.security import generate_password_hash

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@oattao@123",
    database="StockPortfolio"
)

cursor = connection.cursor()

# Insert more users and their stocks
users_stocks = [
    ("john", "johnpassword", 15000.0, [
        ("MSFT", 20),
        ("TSLA", 8),
    ]),
    ("alice", "alicepassword", 12000.0, [
        ("FB", 15),
        ("GOOGL", 4),
        ("AMZN", 3)
    ]),
    ("bob", "bobpassword", 18000.0, [
        ("AAPL", 30),
        ("GOOGL", 7),
        ("TSLA", 9)
    ])
]

for username, password, balance, user_stocks in users_stocks:
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password, balance) VALUES (%s, %s, %s)", (username, hashed_password, balance))
    user_id = cursor.lastrowid

    for stock_name, stock_quantity in user_stocks:
        cursor.execute("INSERT INTO stocks (user_id, stock_name, stock_quantity) VALUES (%s, %s, %s)", (user_id, stock_name, stock_quantity))

connection.commit()
cursor.close()
connection.close()
