import pandas as pd


ALLOWED_PAYMENT_METHODS = {
    "UPI",
    "CARD",
    "NET_BANKING"
}

ALLOWED_BANKS = {
    "AXIS",
    "HDFC",
    "ICICI",
    "KOTAK",
    "SBI"
}

ALLOWED_FAILURE_REASONS = {
    "TIMEOUT",
    "AUTHENTICATION_FAILED",
    "BANK_ERROR",
    "INSUFFICIENT_FUNDS",
    "USER_CANCELLED"
}

ALLOWED_INTERVENTIONS = {
    "RETRY",
    "WAIT",
    "SWITCH_METHOD"
}


def validate_payment(payment):
    """
    Validate a single payment before it reaches
    the Payment Twin model.
    """

    if not isinstance(payment, pd.DataFrame):
        raise TypeError(
            "Payment must be a pandas DataFrame."
        )

    if len(payment) != 1:
        raise ValueError(
            "Payment must contain exactly one row."
        )

    required_columns = [
        "amount",
        "payment_method",
        "bank",
        "hour",
        "response_time",
        "failure_reason",
        "intervention"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in payment.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    row = payment.iloc[0]

    # ---------------------------------------
    # Amount
    # ---------------------------------------

    if pd.isna(row["amount"]):
        raise ValueError(
            "Amount cannot be missing."
        )

    if row["amount"] <= 0:
        raise ValueError(
            "Amount must be greater than zero."
        )

    # ---------------------------------------
    # Payment method
    # ---------------------------------------

    if row["payment_method"] not in ALLOWED_PAYMENT_METHODS:
        raise ValueError(
            f"Invalid payment method: "
            f"{row['payment_method']}"
        )

    # ---------------------------------------
    # Bank
    # ---------------------------------------

    if row["bank"] not in ALLOWED_BANKS:
        raise ValueError(
            f"Invalid bank: {row['bank']}"
        )

    # ---------------------------------------
    # Hour
    # ---------------------------------------

    if pd.isna(row["hour"]):
        raise ValueError(
            "Hour cannot be missing."
        )

    if not 0 <= row["hour"] <= 23:
        raise ValueError(
            "Hour must be between 0 and 23."
        )

    # ---------------------------------------
    # Response time
    # ---------------------------------------

    if pd.isna(row["response_time"]):
        raise ValueError(
            "Response time cannot be missing."
        )

    if row["response_time"] < 0:
        raise ValueError(
            "Response time cannot be negative."
        )

    # ---------------------------------------
    # Failure reason
    # ---------------------------------------

    if row["failure_reason"] not in ALLOWED_FAILURE_REASONS:
        raise ValueError(
            f"Invalid failure reason: "
            f"{row['failure_reason']}"
        )

    # ---------------------------------------
    # Intervention
    # ---------------------------------------

    if row["intervention"] not in ALLOWED_INTERVENTIONS:
        raise ValueError(
            f"Invalid intervention: "
            f"{row['intervention']}"
        )

    return True