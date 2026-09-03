import pandas as pd

from payment_twin import PaymentTwin


# ---------------------------------------
# Create test payment
# ---------------------------------------

payment = pd.DataFrame([{
    "payment_id": "TEST001",
    "amount": 27320,
    "payment_method": "CARD",
    "bank": "KOTAK",
    "hour": 11,
    "response_time": 19.3,
    "failure_reason": "TIMEOUT",
    "intervention": "WAIT"
}])


# ---------------------------------------
# Create Payment Twin
# ---------------------------------------

twin = PaymentTwin()


# ---------------------------------------
# Analyze payment
# ---------------------------------------

result = twin.analyze(
    payment
)


# ---------------------------------------
# Validate
# ---------------------------------------

assert result[
    "payment_id"
] == "TEST001"

assert result[
    "recommended_action"
] in [
    "RETRY",
    "WAIT",
    "SWITCH_METHOD"
]

assert 0 <= result[
    "predicted_recovery"
] <= 1

assert 0 <= result[
    "probability_margin"
] <= 1

assert result[
    "economic_margin"
] >= 0

assert result[
    "priority"
] in [
    "HIGH",
    "MEDIUM",
    "LOW"
]

assert isinstance(
    result["decision_results"],
    pd.DataFrame
)


print("Payment Twin result:")
print(
    f"  Payment: {result['payment_id']}"
)
print(
    f"  Action: {result['recommended_action']}"
)
print(
    f"  Recovery: "
    f"{result['predicted_recovery']:.2%}"
)
print(
    f"  Probability margin: "
    f"{result['probability_margin']:.4f}"
)
print(
    f"  Economic margin: "
    f"{result['economic_margin']:.2f}"
)
print(
    f"  Priority: {result['priority']}"
)
print(
    f"  Expected incremental value: "
    f"{result['expected_incremental_value']:.2f}"
)

print(
    "\nPayment Twin integration test passed."
)