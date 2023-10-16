from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
from p.database_manager import DatabaseManager
from p.utils import get_stock_price, authenticate_user

def login():
    return render_template('index.html')

def sign_in():
    db_manager = DatabaseManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_manager = DatabaseManager()

        if not db_manager.get_password(username):
            hashed_password = generate_password_hash(password)
            db_manager.register_user(username, hashed_password)
            return redirect(url_for('login'))
        else:
            return "Username already exists!", 400

    return render_template('sign_in.html')

def calculate():
    username = request.form['username']
    password = request.form['password']
    db_manager = DatabaseManager()

    if not authenticate_user(username, password, db_manager):
        return "Invalid username or password!", 403

    user_id, portfolio_value = db_manager.calculate_user_portfolio_value(username)
    session['user_id'] = user_id  # Storing user_id in session

    stocks = db_manager.get_stocks(user_id)
    return render_template('result.html', user_id=user_id, user=username, value=portfolio_value, stocks=stocks)

def add_stock():
    if 'user_id' not in session:
        return "User not logged in!", 403

    user_id = session['user_id']
    stock_name = request.form['stock_name']
    stock_quantity = int(request.form['stock_quantity'])
    db_manager = DatabaseManager()

    existing_stock = db_manager.get_specific_stock(user_id, stock_name)
    if existing_stock:
        new_quantity = existing_stock[1] + stock_quantity
        db_manager.update_stock(user_id, stock_name, new_quantity)
    else:
        db_manager.add_stock(user_id, stock_name, stock_quantity)

    return redirect(url_for('calculate'))

def delete_stock():
    if 'user_id' not in session:
        return "User not logged in!", 403

    user_id = session['user_id']
    stock_name = request.form['stock_name']
    db_manager = DatabaseManager()
    
    db_manager.delete_stock(user_id, stock_name)
    return redirect(url_for('calculate'))
