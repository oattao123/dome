import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@oattao@123",
    database="StockPortfolio"
)

cursor = connection.cursor()

# Create users table
cursor.execute("""
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,  # this should store the hashed password
    balance FLOAT DEFAULT 0.0
)
""")

# Create stocks table
cursor.execute("""
CREATE TABLE stocks (
    stock_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    stock_name VARCHAR(255) NOT NULL,
    stock_quantity INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

connection.commit()
cursor.close()
connection.close()
