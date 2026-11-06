import sqlite3
from product_evaluator import calculate_opportunity_score, evaluate_product
from database import connect_database, add_to_watchlist, view_watchlist, remove_from_watchlist, search_product, delete_product, save_product, get_all_products

connection = connect_database()
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    selling_price REAL,
    purchase_price REAL,
    shipping REAL,
    fees REAL,
    profit REAL,
    profit_margin REAL,
    demand TEXT,
    competition TEXT,
    watchlist INTEGER DEFAULT 0
)
""")

connection.commit()

try:
    cursor.execute("ALTER TABLE products ADD COLUMN profit_margin REAL")
    connection.commit()
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE products ADD COLUMN demand TEXT")
    connection.commit()
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE products ADD COLUMN competition TEXT")
    connection.commit()
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE products ADD COLUMN watchlist INTEGER DEFAULT 0")
    connection.commit()
except sqlite3.OperationalError:
    pass

connection.commit()
cursor.execute("""
UPDATE products
SET profit_margin = (profit / selling_price) * 100
WHERE profit_margin IS NULL AND selling_price > 0
""")

connection.commit()

existing_products = get_all_products(connection)

existing_products = [
    {
        "id": product[0],
        "name": product[1],
        "selling_price": product[2],
        "purchase_price": product[3],
        "shipping": product[4],
        "fees": product[5],
        "profit": product[6],
        "profit_margin": product[7],
        "demand": product[8]
    }
    for product in existing_products
]

for product in existing_products:
    profit_score = max(0, min(product["profit"] / 200 * 100, 100))
    margin_score = max(0, min(product["profit_margin"] or 0, 100))

    if product["demand"] == "low":
        demand_score = 25
    elif product["demand"] == "high":
        demand_score = 100
    else:
        demand_score = 60

    if product.get("competition") == "low":
        competition_score = 100
    elif product.get("competition") == "high":
        competition_score = 25
    else:
        competition_score = 60

    product["opportunity_score"] = calculate_opportunity_score(
        product["profit"],
        product["profit_margin"] or 0,
        demand_score,
        competition_score
    )
for product in existing_products:
    print("ID:", product["id"])
    print("Name:", product["name"])
    print("Selling price: $", product["selling_price"])
    print("Purchase price: $", product["purchase_price"])
    print("Shipping: $", product["shipping"])
    print("Fees: $", product["fees"])
    print("Profit: $", product["profit"])
    print("Profit Margin:", round(product["profit_margin"] or 0, 2), "%")
    print("Demand:", product["demand"] or "Not recorded")
    print("-------------------")

def get_number(prompt):
    while True:
        try:
            number = float(input(prompt))

            if number < 0:
                print("Number cannot be negative.")
                continue

            return number

        except ValueError:
            print("Please enter a valid number.")

saved_products = []
while True:

    product = input("Enter product name (or q to quit): ")

    if product.lower() == "search":
        search_name = input("What product are you looking for? ")

        results = search_product(connection, search_name)

        if results:
            for item in results:
                print(item)
        else:
            print("No products found.")

        continue

    if product.lower() == "delete":
        try:
            product_id = int(input("Enter the ID of the product to delete: "))

            success = delete_product(connection, product_id)

            if success:
                print("Product deleted successfully!")
            else:
                print("Product ID not found.")

        except ValueError:
            print("Please enter a valid product ID.")

        continue

    if product.lower() == "watchlist":
        try:
            product_id = int(input("Enter product ID to watchlist: "))

            success = add_to_watchlist(connection, product_id)

            if success:
                print("Product added to watchlist!")
            else:
                print("Product ID not found.")

        except ValueError:
            print("Please enter a valid product ID.")

        continue

    if product.lower() == "viewwatchlist":
        products = view_watchlist(connection)

        if products:
            print("\n--- YOUR WATCHLIST ---")

            for item in products:
                print("ID:", item[0])
                print("Product:", item[1])
                print("Current Profit: $", item[2])
                print("--------------------")
        else:
            print("Your watchlist is empty.")

        continue

    if product.lower() == "removewatchlist":
        try:
            product_id = int(input("Enter product ID to remove from watchlist: "))

            success = remove_from_watchlist(connection, product_id)

            if success:
                print("Product removed from watchlist!")
            else:
                print("Product not found on watchlist.")

        except ValueError:
            print("Please enter a valid product ID.")

        continue

    if product.lower() == "q":
        break

    selling_price = get_number("Enter selling price: ")
    purchase_price = get_number("Enter purchase price: ")
    shipping = get_number("Enter shipping cost: ")
    fees = get_number("Enter marketplace fees: ")
    demand = input("How strong is the product demand? (Low, Medium, High): ").lower()
    competition = input("How competitive is the market? (Low, Medium, High): ").lower()
    if demand == "low":
        demand_score = 25

    elif demand == "medium":
        demand_score = 60

    elif demand == "high":
        demand_score = 100
    else:
        print("Invalid demand rating. Using Medium.")
        demand_score = 60

    if competition == "low":
        competition_score = 100
    elif competition == "medium":
        competition_score = 60
    elif competition == "high":
        competition_score = 25
    else:
        print("Invalid competition rating. Using Medium.")
        competition_score = 60

    result = evaluate_product(product, selling_price, purchase_price, shipping, fees)

    if selling_price > 0:
        profit_margin = (result[0] / selling_price) * 100
    else:
        profit_margin = 0

    saved_product = {
        "name": product,
        "selling_price": selling_price,
        "purchase_price": purchase_price,
        "shipping": shipping,
        "fees": fees,
        "profit": result[0],
        "profit_margin": profit_margin,
        "demand": demand,
        "competition": competition,

        "opportunity_score": calculate_opportunity_score(
            result[0],
            profit_margin,
            demand_score,
            competition_score
        ),
        "decision": result[1]
    }


    product_id = save_product(connection, saved_product)
    print("Product saved with ID:", product_id)

    saved_products.append(saved_product)

    print("----------------------")
    print("Product:", product)
    print("Profit: $", result[0])
    print("Profit Margin:", round(profit_margin, 2), "%")
    print("Opportunity Score:", round(saved_product["opportunity_score"], 2), "/100")
    print("Demand:", saved_product["demand"])
    print("Competition:", saved_product["competition"])
    print("Decision:", result[1])
    print("----------------------")

all_products = existing_products + saved_products

print("\nHOW WOULD YOU LIKE TO RANK PRODUCTS?")
print("1. Highest Profit")
print("2. Highest Profit Margin")
print("3. Best Overall Opportunity")

ranking_choice = input("Choose 1, 2, or 3: ")
if ranking_choice == "1":
    all_products.sort(key=lambda x: x["profit"], reverse=True)
    print("\nRanking by highest profit.")

elif ranking_choice == "2":
    all_products.sort(key=lambda x: x["profit_margin"], reverse=True)
    print("\nRanking by highest profit margin.")

elif ranking_choice == "3":
    all_products.sort(key=lambda x: x["opportunity_score"], reverse=True)
    print("\nRanking by best overall opportunity.")

else:
    print("Invalid choice. Ranking by highest profit.")
    all_products.sort(key=lambda x: x["profit"], reverse=True)

print("\nYOUR SAVED PRODUCTS")
for saved_product in all_products:
    print("Product:", saved_product["name"])
    print("Selling price: $", saved_product["selling_price"])
    print("Purchase price: $", saved_product["purchase_price"])
    print("Shipping: $", saved_product["shipping"])
    print("Fees: $", saved_product["fees"])
    print("Profit: $", saved_product["profit"])
    print("Profit margin:", f"{saved_product['profit_margin'] or 0:.2f}%")
    print("Opportunity Score:", round(saved_product["opportunity_score"], 2), "/100")
    print("Decision:", saved_product.get("decision", "Not recorded"))
    print("Demand:", saved_product.get("demand") or "Not recorded")
    print("Competition:", saved_product.get("competition") or "Not recorded")
    print("-------------------")

connection.close()