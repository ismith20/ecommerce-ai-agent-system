from database import connect_database, get_all_products
from product_evaluator import calculate_opportunity_score
import json
from ai_analyzer import analyze_products

connection = connect_database()

products = get_all_products(connection)

print("Products found:", len(products))

profitable_products = []
demand_scores = {
    "low": 25,
    "medium": 60,
    "high": 100
}

competition_scores = {
    "low": 100,
    "medium": 60,
    "high": 25
}
scored_products = []
detailed_products = []

for product in products:
    if product[6] > 0:
        profitable_products.append(product)

        demand = (product[8] or "medium").lower()
        competition = (product[9] or "medium").lower()

        demand_score = demand_scores.get(demand, 60)
        competition_score = competition_scores.get(competition, 60)

        opportunity_score = calculate_opportunity_score(
            product[6],
            product[7] or 0,
            demand_score,
            competition_score
        )
        scored_products.append((product[1], opportunity_score))
        detailed_products.append({
            "id": product[0],
            "name": product[1],
            "selling_price": product[2],
            "purchase_price": product[3],
            "shipping": product[4],
            "fees": product[5],
            "profit": product[6],
            "profit_margin": product[7] or 0,
            "demand": product[8] or "Not recorded",
            "competition": product[9] or "Not recorded",
            "opportunity_score": round(opportunity_score, 2)
        })
        print("Profitable Product:", product[1])
        print("Profit: $", product[6])
        print("Opportunity Score:", round(opportunity_score, 2), "/100")
        print("--------------------")

scored_products.sort(key=lambda item: item[1], reverse=True)

print("\n--- RANKED PRODUCT OPPORTUNITIES ---")

for name, score in scored_products:
    print("Product:", name)
    print("Opportunity Score:", round(score, 2), "/100")
    print("--------------------")

report = sorted(
    detailed_products,
    key=lambda item: item["opportunity_score"],
    reverse=True
)

print("\n--- MANAGER AGENT JSON REPORT ---")
print(json.dumps(report, indent=4))

with open("manager_report.json", "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("Manager report saved successfully!")
print("\n--- AI MANAGER ANALYSIS ---")

analysis = analyze_products(report)

print(analysis)

connection.close()