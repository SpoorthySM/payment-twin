import joblib
import pandas as pd

from decision_engine import evaluate_actions


# Load our trained model
model = joblib.load(
    "models/calibrated_model.pkl"
)


# Example failed payment
payment = pd.DataFrame([{
    "amount": 27320,
    "payment_method": "CARD",
    "bank": "KOTAK",
    "hour": 11,
    "response_time": 19.3,
    "failure_reason": "TIMEOUT",
}])


# Evaluate possible actions
recommendation, results, probability_margin, economic_margin = evaluate_actions(    model,
    payment
)


print("\nRecommended action:", recommendation)

print("Probability margin:", probability_margin)
print("Economic margin:", economic_margin)
print("\nResults:")

print(
    results[
        [
            "intervention",
            "predicted_recovery",
            "expected_recovered_value",
            "action_cost",
            "decision_score"
        ]
    ]
)
