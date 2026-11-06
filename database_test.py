import sqlite3

connection = sqlite3.connect("products.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM products WHERE name = ?", ("Gaming Keyboard",))

products = cursor.fetchall()

for product in products:
    print(product)

connection.close()