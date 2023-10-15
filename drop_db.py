import mysql.connector

def drop_tables():
    # Establish a connection to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@oattao@123",
        database="StockPortfolio"
    )
    
    cursor = connection.cursor()

    try:
        # Drop the 'stocks' table first due to the foreign key constraint
        cursor.execute("DROP TABLE IF EXISTS stocks;")
        # Then drop the 'users' table
        cursor.execute("DROP TABLE IF EXISTS users;")
        print("Tables 'users' and 'stocks' have been dropped successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and the connection
        cursor.close()
        connection.close()

# Call the function to drop the tables
drop_tables()

