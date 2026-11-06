import sqlite3

def connect_database():
    connection = sqlite3.connect("products.db")
    return connection

def add_to_watchlist(connection, product_id):
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE products
    SET watchlist = 1
    WHERE id = ?
    """, (product_id,))

    connection.commit()

    return cursor.rowcount > 0

def view_watchlist(connection):
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, name, profit
    FROM products
    WHERE watchlist = 1
    """)

    products = cursor.fetchall()

    return products

def remove_from_watchlist(connection, product_id):
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE products
    SET watchlist = 0
    WHERE id = ? AND watchlist = 1
    """, (product_id,))

    connection.commit()

    return cursor.rowcount > 0

def search_product(connection, product_name):
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE name LIKE ?",
        (f"%{product_name}%",)
    )

    results = cursor.fetchall()

    return results

def delete_product(connection, product_id):
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    connection.commit()

    return cursor.rowcount > 0

def save_product(connection, product_data):
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO products (
        name, selling_price, purchase_price,
        shipping, fees, profit, profit_margin,
        demand, competition
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product_data["name"],
        product_data["selling_price"],
        product_data["purchase_price"],
        product_data["shipping"],
        product_data["fees"],
        product_data["profit"],
        product_data["profit_margin"],
        product_data["demand"],
        product_data["competition"]
    ))

    connection.commit()

    return cursor.lastrowid

def get_all_products(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    return products