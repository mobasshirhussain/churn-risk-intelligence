import pandas as pd

def generate_retention_strategies(model, input_df):

    base_prob = model.predict_proba(input_df)[0][1]
    strategies = []

    # Strategy 1: Loyalty Reward Program
    modified = input_df.copy()
    modified["Tenure"] = (modified["Tenure"] + 2).clip(upper=10)
    new_prob = model.predict_proba(modified)[0][1]

    if new_prob < base_prob:
        strategies.append("Offer Loyalty Reward Program to increase customer engagement.")

    # Strategy 2: Balance Protection Offer
    modified = input_df.copy()
    modified["Balance"] = modified["Balance"] * 0.8
    new_prob = model.predict_proba(modified)[0][1]

    if new_prob < base_prob:
        strategies.append("Provide Balance Protection Plan or Financial Advisory Service.")

    # Strategy 3: Premium Service Upgrade
    modified = input_df.copy()
    modified["NumOfProducts"] = (modified["NumOfProducts"] + 1).clip(upper=4)
    new_prob = model.predict_proba(modified)[0][1]

    if new_prob < base_prob:
        strategies.append("Promote Premium Banking Products for higher engagement.")

    # Strategy 4: Engagement Campaign (only if inactive)
    if input_df["IsActiveMember"].iloc[0] == 0:
        modified = input_df.copy()
        modified["IsActiveMember"] = 1
        new_prob = model.predict_proba(modified)[0][1]

        if new_prob < base_prob:
            strategies.append("Launch Personalized Engagement Campaign.")

    return strategies
