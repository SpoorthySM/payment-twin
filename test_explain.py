import pandas as pd

from explain import explain_payment


# ---------------------------------------
# Create test payment
# ---------------------------------------

payment = pd.DataFrame([{
    "amount": 27320,
    "payment_method": "CARD",
    "bank": "KOTAK",
    "hour": 11,
    "response_time": 19.3,
    "failure_reason": "TIMEOUT",
    "intervention": "WAIT"
}])


# ---------------------------------------
# Generate explanation
# ---------------------------------------

explanation = explain_payment(
    payment,
    top_n=5
)


# ---------------------------------------
# Validate
# ---------------------------------------

assert isinstance(
    explanation,
    pd.DataFrame
)

assert len(explanation) == 5

assert "feature" in explanation.columns

assert "shap_value" in explanation.columns

assert "absolute_shap" in explanation.columns

assert "human_feature" in explanation.columns

assert explanation[
    "absolute_shap"
].is_monotonic_decreasing


print("Top SHAP features:")
print(explanation[
    [
        "feature",
        "shap_value"
    ]
].to_string(index=False))


print(
    "\nSHAP explanation test passed."
)

print(
    explanation[
        [
            "human_feature",
            "shap_value"
        ]
    ].to_string(index=False)
)