import joblib
import pandas as pd
import shap


MODEL_PATH = "models/calibrated_model.pkl"


def load_explainer():
    """
    Load the saved calibrated model and create a SHAP
    TreeExplainer for one underlying XGBoost model.

    The calibrated model is used for the final probability.
    SHAP explains the underlying XGBoost prediction.
    """

    model = joblib.load(
        MODEL_PATH
    )

    calibrated_estimator = (
        model.calibrated_classifiers_[0]
    )

    pipeline = calibrated_estimator.estimator

    xgb_model = pipeline.named_steps[
        "classifier"
    ]

    explainer = shap.TreeExplainer(
        xgb_model
    )

    return (
        model,
        pipeline,
        explainer
    )


def get_shap_values(
    payment,
    explainer,
    pipeline
):
    """
    Calculate SHAP values for one payment.
    """

    transformed = pipeline.named_steps[
        "preprocessor"
    ].transform(payment)

    shap_values = explainer.shap_values(
        transformed
    )

    if isinstance(
        shap_values,
        list
    ):
        shap_values = shap_values[0]

    shap_values = shap_values[0]

    feature_names = (
        pipeline.named_steps[
            "preprocessor"
        ].get_feature_names_out()
    )

    result = pd.DataFrame({
        "feature": feature_names,
        "shap_value": shap_values
    })

    result["absolute_shap"] = (
        result["shap_value"].abs()
    )

    result = result.sort_values(
        "absolute_shap",
        ascending=False
    ).reset_index(
        drop=True
    )

    return result


def humanize_feature_name(
    feature
):
    """
    Convert model-generated feature names
    into human-readable descriptions.
    """

    if feature.startswith(
        "cat__failure_reason_"
    ):
        reason = feature.replace(
            "cat__failure_reason_",
            ""
        )

        return (
            "Failure reason: "
            + reason.replace(
                "_",
                " "
            ).title()
        )

    if feature.startswith(
        "cat__intervention_"
    ):
        intervention = feature.replace(
            "cat__intervention_",
            ""
        )

        return (
            "Intervention: "
            + intervention.replace(
                "_",
                " "
            ).title()
        )

    if feature.startswith(
        "cat__payment_method_"
    ):
        method = feature.replace(
            "cat__payment_method_",
            ""
        )

        return (
            "Payment method: "
            + method.replace(
                "_",
                " "
            ).title()
        )

    if feature.startswith(
        "cat__bank_"
    ):
        bank = feature.replace(
            "cat__bank_",
            ""
        )

        return "Bank: " + bank

    if feature.startswith(
        "remainder__"
    ):
        feature = feature.replace(
            "remainder__",
            ""
        )

    return feature.replace(
        "_",
        " "
    ).title()


def explain_payment(
    payment,
    top_n=5
):
    """
    Generate the top feature contributions
    for a payment.
    """

    (
        model,
        pipeline,
        explainer
    ) = load_explainer()

    shap_result = get_shap_values(
        payment,
        explainer,
        pipeline
    )

    result = shap_result.head(
        top_n
    ).copy()

    result["human_feature"] = (
        result["feature"]
        .apply(
            humanize_feature_name
        )
    )

    return result