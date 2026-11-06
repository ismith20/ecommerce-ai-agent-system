import json

with open("manager_report.json", "r", encoding="utf-8") as file:
    products = json.load(file)

research_queue = []

for product in products[:5]:
    research_queue.append({
        "id": product["id"],
        "name": product["name"],
        "status": "needs_verification"
    })

with open("research_queue.json", "w", encoding="utf-8") as file:
    json.dump(research_queue, file, indent=4)

print("Research queue created!")
print("Products awaiting research:", len(research_queue))