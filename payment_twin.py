import joblib
import pandas as pd
from validation import validate_payment
from explain import explain_payment
from decision_engine import evaluate_actions
from prioritization import (
    calculate_priority,
    priority_level
)


class PaymentTwin:

    def __init__(
        self,
        model_path="models/calibrated_model.pkl"
    ):
        """
        Load the trained Payment Twin recovery model.
        """

        self.model = joblib.load(
            model_path
        )

    def analyze(self, payment):
        """
        Analyze one failed payment.

        Parameters
        ----------
        payment : pandas.DataFrame
            One-row DataFrame containing the payment features.

        Returns
        -------
        dict
            Complete Payment Twin analysis.
        """

        # ---------------------------------------
        # Validate input
        # ---------------------------------------

        if not isinstance(
            payment,
            pd.DataFrame
        ):
            raise TypeError(
                "payment must be a pandas DataFrame"
            )

        if len(payment) != 1:
            raise ValueError(
                "payment must contain exactly one row"
            )
        validate_payment(
            payment
        )

        # ---------------------------------------
        # Evaluate interventions
        # ---------------------------------------

        (
            recommendation,
            decision_results,
            probability_margin,
            economic_margin
        ) = evaluate_actions(
            self.model,
            payment
        )

        # ---------------------------------------
        # Generate explanation
        # ---------------------------------------

        explanation = explain_payment(
            payment,
            top_n=5
        )

        # ---------------------------------------
        # Get recommended probability
        # ---------------------------------------

        recommended_row = (
            decision_results[
                decision_results[
                    "intervention"
                ] == recommendation
            ]
            .iloc[0]
        )

        predicted_recovery = (
            recommended_row[
                "predicted_recovery"
            ]
        )

        # ---------------------------------------
        # Calculate priority
        # ---------------------------------------

        priority = calculate_priority(
            payment,
            predicted_recovery,
            recommendation
        )

        level = priority_level(
            predicted_recovery,
            priority[
                "expected_incremental_value"
            ]
        )

        # ---------------------------------------
        # Return complete result
        # ---------------------------------------

        return {
            "payment_id": payment.get(
                "payment_id",
                pd.Series([None])
            ).iloc[0],

            "recommended_action": recommendation,

            "predicted_recovery": float(
                predicted_recovery
            ),

            "probability_margin": float(
                probability_margin
            ),

            "economic_margin": float(
                economic_margin
            ),

            "incremental_recovery": float(
                priority[
                    "incremental_recovery"
                ]
            ),

            "action_cost": float(
                priority[
                    "action_cost"
                ]
            ),

            "expected_incremental_value": float(
                priority[
                    "expected_incremental_value"
                ]
            ),

            "priority": level,

            "explanation": explanation,

            "decision_results": decision_results
        }

def action_table(self, payment):
    """
    Return the what-if intervention comparison
    for display in the application.
    """

    result = self.analyze(
        payment
    )

    return result[
        "decision_results"
    ][
        [
            "intervention",
            "predicted_recovery",
            "expected_recovered_value",
            "action_cost",
            "decision_score"
        ]
    ].copy()