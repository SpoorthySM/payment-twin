import pandas as pd

from portfolio import (
    build_recovery_queue,
    evaluate_capacity,
    summarize_queue
)


# ---------------------------------------
# Create representative policy data
# ---------------------------------------

policy_decisions = pd.DataFrame([
    {
        "payment_id": "P001",
        "amount": 50000,
        "recommended_action": "WAIT",
        "predicted_recovery": 0.82,
        "expected_incremental_value": 35000,
        "priority": "HIGH"
    },
    {
        "payment_id": "P002",
        "amount": 30000,
        "recommended_action": "SWITCH_METHOD",
        "predicted_recovery": 0.65,
        "expected_incremental_value": 18000,
        "priority": "MEDIUM"
    },
    {
        "payment_id": "P003",
        "amount": 10000,
        "recommended_action": "RETRY",
        "predicted_recovery": 0.40,
        "expected_incremental_value": 3000,
        "priority": "LOW"
    }
])


# ---------------------------------------
# Build queue
# ---------------------------------------

queue = build_recovery_queue(
    policy_decisions
)


assert len(queue) == 3

assert "rank" in queue.columns

assert queue.iloc[0]["payment_id"] == "P001"

assert (
    queue.iloc[0]["expected_incremental_value"]
    >=
    queue.iloc[1]["expected_incremental_value"]
)


# ---------------------------------------
# Test priority filtering
# ---------------------------------------

high_queue = build_recovery_queue(
    policy_decisions,
    min_priority="HIGH"
)

assert len(high_queue) == 1

assert (
    high_queue.iloc[0]["priority"]
    == "HIGH"
)


# ---------------------------------------
# Test capacity
# ---------------------------------------

capacity_result = evaluate_capacity(
    queue,
    capacity=0.50
)

assert (
    capacity_result["payments_handled"]
    == 1
)

assert (
    capacity_result[
        "expected_incremental_value"
    ]
    == 35000
)


# ---------------------------------------
# Test summary
# ---------------------------------------

summary = summarize_queue(
    queue
)

assert summary["payments"] == 3

assert (
    summary["total_expected_value"]
    == 56000
)

assert (
    0 < summary[
        "average_predicted_recovery"
    ] < 1
)


# ---------------------------------------
# Output
# ---------------------------------------

print("Recovery queue:")
print(queue.to_string(index=False))

print("\nCapacity result:")
print(capacity_result)

print("\nQueue summary:")
print(summary)

print(
    "\nPortfolio test passed."
)