import pandas as pd

from prioritization import (
    calculate_priority,
    priority_level
)


# ---------------------------------------
# Test payment
# ---------------------------------------

payment = pd.DataFrame([{
    "amount": 27320
}])


predicted_recovery = 0.771953

recommended_action = "WAIT"


# ---------------------------------------
# Calculate priority
# ---------------------------------------

result = calculate_priority(
    payment,
    predicted_recovery,
    recommended_action
)


# ---------------------------------------
# Validate result
# ---------------------------------------

assert 0 <= result["incremental_recovery"] <= 1

assert result["action_cost"] == 10

assert (
    result["expected_incremental_value"]
    > 0
)


# ---------------------------------------
# Priority level
# ---------------------------------------

level = priority_level(
    predicted_recovery,
    result["expected_incremental_value"]
)

assert level in [
    "HIGH",
    "MEDIUM",
    "LOW"
]


print("Priority result:")
print(result)

print(
    f"Priority level: {level}"
)

print(
    "Prioritization test passed."
)