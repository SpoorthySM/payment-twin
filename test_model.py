import joblib
import pandas as pd


# ---------------------------------------
# Load trained model
# ---------------------------------------

model = joblib.load(
    "models/calibrated_model.pkl"
)


# ---------------------------------------
# Create a representative failed payment
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
# Predict recovery probability
# ---------------------------------------

probability = model.predict_proba(
    payment
)[0, 1]


# ---------------------------------------
# Validate prediction
# ---------------------------------------

assert 0 <= probability <= 1, (
    "Recovery probability must be between 0 and 1"
)

assert isinstance(
    probability,
    float
), "Prediction should be a float"


print(
    f"Recovery probability: {probability:.2%}"
)

print(
    "Model test passed."
)
