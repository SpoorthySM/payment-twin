import pandas as pd


# ---------------------------------------
# Configuration
# ---------------------------------------

NO_ACTION_BASELINE = 0.03085966201322557

ACTION_COSTS = {
    "RETRY": 20,
    "WAIT": 10,
    "SWITCH_METHOD": 35
}


# ---------------------------------------
# Calculate priority
# ---------------------------------------

def calculate_priority(
    payment,
    predicted_recovery,
    recommended_action
):
    """
    Calculate the operational priority of a failed payment.

    The score estimates the incremental recovery opportunity
    relative to the observed NO_ACTION baseline and accounts
    for intervention cost.

    This is a prioritization score, NOT a causal treatment effect.
    """

    amount = payment["amount"].iloc[0]

    incremental_recovery = (
        predicted_recovery
        - NO_ACTION_BASELINE
    )

    # Do not allow negative estimated benefit
    incremental_recovery = max(
        0.0,
        incremental_recovery
    )

    action_cost = ACTION_COSTS[
        recommended_action
    ]

    expected_incremental_value = (
        amount
        * incremental_recovery
        - action_cost
    )

    return {
        "incremental_recovery": incremental_recovery,
        "action_cost": action_cost,
        "expected_incremental_value": (
            expected_incremental_value
        )
    }


# ---------------------------------------
# Priority level
# ---------------------------------------

def priority_level(
    predicted_recovery,
    expected_incremental_value
):
    """
    Convert the numerical priority score into
    an operational priority level.

    Thresholds are intentionally simple for the
    first production version.
    """

    if (
        predicted_recovery >= 0.70
        and expected_incremental_value >= 500
    ):
        return "HIGH"

    if (
        predicted_recovery >= 0.40
        or expected_incremental_value >= 250
    ):
        return "MEDIUM"

    return "LOW"