import pandas as pd


# Simulation assumptions.
# These are not real payment-provider costs.
ACTION_COSTS = {
    "RETRY": 20,
    "WAIT": 10,
    "SWITCH_METHOD": 35
}


def evaluate_actions(model, payment):
    """
    Evaluate RETRY, WAIT and SWITCH_METHOD for a failed payment.

    The model predicts recovery probability for each hypothetical
    intervention. We then convert that probability into an expected
    recovered value and subtract the simulated intervention cost.

    Parameters
    ----------
    model : trained sklearn-compatible model
        Calibrated recovery prediction model.

    payment : pandas.DataFrame
        One-row payment containing the features expected by the model.

    Returns
    -------
    recommendation : str
        Recommended intervention.

    results : pandas.DataFrame
        What-if analysis for all possible interventions.

    probability_margin : float
        Difference between the best and second-best recovery
        probabilities.

    economic_margin : float
        Difference between the best and second-best economic
        decision scores.
    """

    actions = [
        "RETRY",
        "WAIT",
        "SWITCH_METHOD"
    ]

    scenarios = []

    for action in actions:

        scenario = payment.copy()

        scenario["intervention"] = action

        scenarios.append(scenario)

    what_if = pd.concat(
        scenarios,
        ignore_index=True
    )

    # ---------------------------------------
    # Predict recovery probabilities
    # ---------------------------------------

    probabilities = model.predict_proba(
        what_if
    )[:, 1]

    what_if["predicted_recovery"] = probabilities

    # ---------------------------------------
    # Expected recovered value
    # ---------------------------------------

    amount = payment["amount"].iloc[0]

    what_if["expected_recovered_value"] = (
        what_if["predicted_recovery"]
        * amount
    )

    # ---------------------------------------
    # Intervention cost
    # ---------------------------------------

    what_if["action_cost"] = (
        what_if["intervention"]
        .map(ACTION_COSTS)
    )

    # ---------------------------------------
    # Economic decision score
    # ---------------------------------------

    what_if["decision_score"] = (
        what_if["expected_recovered_value"]
        - what_if["action_cost"]
    )

    # ---------------------------------------
    # Economic recommendation
    # ---------------------------------------

    sorted_economic = what_if.sort_values(
        "decision_score",
        ascending=False
    ).reset_index(drop=True)

    recommendation = sorted_economic.iloc[0][
        "intervention"
    ]

    economic_margin = (
        sorted_economic.iloc[0]["decision_score"]
        -
        sorted_economic.iloc[1]["decision_score"]
    )

    # ---------------------------------------
    # Probability margin
    # ---------------------------------------

    sorted_probability = what_if.sort_values(
        "predicted_recovery",
        ascending=False
    ).reset_index(drop=True)

    probability_margin = (
        sorted_probability.iloc[0]["predicted_recovery"]
        -
        sorted_probability.iloc[1]["predicted_recovery"]
    )

    return (
        recommendation,
        what_if,
        probability_margin,
        economic_margin
    )
