import pandas as pd

from validation import validate_payment


def valid_payment():
    return pd.DataFrame([{
        "amount": 27320,
        "payment_method": "CARD",
        "bank": "KOTAK",
        "hour": 11,
        "response_time": 19.3,
        "failure_reason": "TIMEOUT",
        "intervention": "WAIT"
    }])


# Valid payment should pass

assert validate_payment(
    valid_payment()
) is True


# Negative amount should fail

payment = valid_payment()
payment.loc[0, "amount"] = -100

try:
    validate_payment(payment)
    raise AssertionError(
        "Negative amount was accepted."
    )
except ValueError:
    pass


# Invalid hour should fail

payment = valid_payment()
payment.loc[0, "hour"] = 25

try:
    validate_payment(payment)
    raise AssertionError(
        "Invalid hour was accepted."
    )
except ValueError:
    pass


# Negative response time should fail

payment = valid_payment()
payment.loc[0, "response_time"] = -5

try:
    validate_payment(payment)
    raise AssertionError(
        "Negative response time was accepted."
    )
except ValueError:
    pass


# Invalid payment method should fail

payment = valid_payment()
payment.loc[0, "payment_method"] = "INVALID"

try:
    validate_payment(payment)
    raise AssertionError(
        "Invalid payment method was accepted."
    )
except ValueError:
    pass


print(
    "Validation tests passed."
)