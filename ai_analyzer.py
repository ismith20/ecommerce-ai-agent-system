
import json
from openai import OpenAI

def analyze_products(products):
    client = OpenAI()

    response = client.responses.create(
        model="gpt-6-luna",
        input=f"""
        You are an ecommerce product research analyst.

        Review these products:

        {json.dumps(products[:5], indent=2)}

        Identify the strongest opportunity.

        Explain the profit, demand, and competition.

        Demand and competition ratings are manually
        entered and have not been verified.

        Recommend what should be researched next.

        Do not invent market data.
        Keep your response concise.
        """,
        reasoning={"effort": "none"},
        max_output_tokens=300
    )

    return response.output_text
