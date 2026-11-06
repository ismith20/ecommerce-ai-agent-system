import json
from openai import OpenAI
with open("manager_report.json", "r", encoding="utf-8") as file:
    products = json.load(file)

print("Products loaded:", len(products))
client = OpenAI()

response = client.responses.create(
    model="gpt-6-luna",
    input=f"""
    You are an ecommerce product research assistant.

    Analyze these products from my database:

    {json.dumps(products[:5], indent=2)}

    Identify the highest-ranked product and explain
    why it deserves further research.

    Only use the information provided.
    Do not invent sales, demand, or market trends.
    Keep your response short.
    """,
    reasoning={"effort": "none"},
    max_output_tokens=250
)

print(response.output_text)
