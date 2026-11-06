def calculate_opportunity_score(profit, profit_margin, demand_score, competition_score):
    if profit <= 0:
        return 0
    profit_score = max(0, min(profit / 200 * 100, 100))
    margin_score = max(0, min(profit_margin, 100))

    opportunity_score = (
        profit_score * 0.35
        + margin_score * 0.25
        + demand_score * 0.25
        + competition_score * 0.15
    )
    return opportunity_score
def evaluate_product(product, selling_price, purchase_price, shipping, fees):
    profit = selling_price - purchase_price - shipping - fees

    if profit >= 20:
        decision = "GOOD OPPORTUNITY"
    elif profit >= 10:
        decision = "POTENTIAL OPPORTUNITY"
    else:
        decision = "LOW PROFIT OPPORTUNITY"

    return profit, decision