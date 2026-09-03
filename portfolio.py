import pandas as pd


# ---------------------------------------
# Priority ordering
# ---------------------------------------

PRIORITY_ORDER = {
    "HIGH": 0,
    "MEDIUM": 1,
    "LOW": 2
}


# ---------------------------------------
# Build recovery queue
# ---------------------------------------

def build_recovery_queue(
    policy_decisions,
    min_priority=None
):
    """
    Build a ranked recovery opportunity queue.

    Payments are first ordered by priority
    (HIGH → MEDIUM → LOW), and then by
    expected incremental value within each
    priority level.
    """

    required_columns = [
        "payment_id",
        "amount",
        "recommended_action",
        "predicted_recovery",
        "expected_incremental_value",
        "priority"
    ]

    missing = [
        column
        for column in required_columns
        if column not in policy_decisions.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    queue = policy_decisions[
        required_columns
    ].copy()

    # -----------------------------------
    # Validate priority values
    # -----------------------------------

    invalid_priorities = (
        set(queue["priority"].dropna().unique())
        - set(PRIORITY_ORDER.keys())
    )

    if invalid_priorities:
        raise ValueError(
            f"Invalid priority values: "
            f"{sorted(invalid_priorities)}"
        )

    # -----------------------------------
    # Optional priority filtering
    # -----------------------------------

    if min_priority is not None:

        if min_priority not in PRIORITY_ORDER:
            raise ValueError(
                "min_priority must be HIGH, "
                "MEDIUM, or LOW"
            )

        queue["_priority_order"] = (
            queue["priority"]
            .map(PRIORITY_ORDER)
        )

        queue = queue[
            queue["_priority_order"]
            <= PRIORITY_ORDER[min_priority]
        ].copy()

        queue = queue.drop(
            columns="_priority_order"
        )

    # -----------------------------------
    # Rank the queue
    # -----------------------------------

    queue["_priority_order"] = (
        queue["priority"]
        .map(PRIORITY_ORDER)
    )

    queue = queue.sort_values(
        [
            "_priority_order",
            "expected_incremental_value"
        ],
        ascending=[
            True,
            False
        ]
    ).drop(
        columns="_priority_order"
    ).reset_index(
        drop=True
    )

    # -----------------------------------
    # Add ranking
    # -----------------------------------

    queue.insert(
        0,
        "rank",
        range(
            1,
            len(queue) + 1
        )
    )

    return queue


# ---------------------------------------
# Evaluate intervention capacity
# ---------------------------------------

def evaluate_capacity(
    queue,
    capacity
):
    """
    Evaluate how many recovery opportunities
    can be handled at a given intervention
    capacity.

    capacity must be between 0 and 1.

    Example:
        capacity=0.10
        means the intervention team can
        handle 10% of the available queue.
    """

    if not 0 < capacity <= 1:
        raise ValueError(
            "capacity must be between 0 and 1"
        )

    if len(queue) == 0:

        return {
            "capacity": capacity,
            "payments_handled": 0,
            "expected_incremental_value": 0.0
        }

    payments_handled = max(
        1,
        int(
            len(queue) * capacity
        )
    )

    selected = queue.head(
        payments_handled
    )

    expected_value = (
        selected[
            "expected_incremental_value"
        ].sum()
    )

    return {
        "capacity": capacity,
        "payments_handled": payments_handled,
        "expected_incremental_value": float(
            expected_value
        )
    }


# ---------------------------------------
# Summarize queue
# ---------------------------------------

def summarize_queue(
    queue
):
    """
    Generate portfolio-level summary
    statistics.
    """

    if len(queue) == 0:

        return {
            "payments": 0,
            "total_expected_value": 0.0,
            "average_predicted_recovery": 0.0
        }

    return {
        "payments": len(queue),

        "total_expected_value": float(
            queue[
                "expected_incremental_value"
            ].sum()
        ),

        "average_predicted_recovery": float(
            queue[
                "predicted_recovery"
            ].mean()
        )
    }