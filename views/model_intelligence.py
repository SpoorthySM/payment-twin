import streamlit as st
import joblib

from components.styles import render_html


# ============================================================
# MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load(
        "models/calibrated_model.pkl"
    )


@st.cache_resource
def load_feature_names():
    return joblib.load(
        "models/feature_names.pkl"
    )


model = load_model()
feature_names = load_feature_names()


# ============================================================
# HELPERS
# ============================================================

def get_classifier():

    estimator = model.estimator

    if hasattr(estimator, "named_steps"):

        return estimator.named_steps.get(
            "classifier"
        )

    return estimator


def render_metric_card(
    label,
    value,
    description,
    value_class="tw-blue"
):

    render_html(
        f"""
        <div class="tw-card"
             style="
                 min-height:155px;
                 display:flex;
                 flex-direction:column;
             ">

            <div class="tw-card-title">
                {label}
            </div>

            <div class="tw-big-number {value_class}">
                {value}
            </div>

            <div style="
                color:#7D898D;
                font-size:0.72rem;
                line-height:1.45;
                margin-top:0.5rem;
            ">
                {description}
            </div>

        </div>
        """
    )


# ============================================================
# PAGE HEADER
# ============================================================

def render_page_header():

    render_html(
        """
        <div style="
            margin-bottom:2.2rem;
        ">

            <div class="tw-eyebrow">
                MODEL INTELLIGENCE
            </div>

            <div class="tw-title">
                The model behind every
                recovery decision.
            </div>

            <div class="tw-subtitle">
                Payment Twin combines calibrated recovery probabilities
                with economic decisioning to select the intervention
                with the highest expected value.
            </div>

            <div class="tw-line"></div>

        </div>
        """
    )


# ============================================================
# MODEL OVERVIEW
# ============================================================

def render_model_overview():

    classifier = get_classifier()

    model_name = type(
        classifier
    ).__name__

    calibration_name = type(
        model
    ).__name__

    feature_count = len(
        feature_names
    )

    cols = st.columns(
        4,
        gap="medium"
    )

    with cols[0]:

        render_metric_card(
            "MODEL",
            "XGBOOST",
            "Recovery prediction engine",
            "tw-blue"
        )

    with cols[1]:

        render_metric_card(
            "CALIBRATION",
            "5-FOLD",
            "Probability calibration layer",
            "tw-positive"
        )

    with cols[2]:

        render_metric_card(
            "FEATURES",
            str(feature_count),
            "Transformed model features",
            "tw-blue"
        )

    with cols[3]:

        render_metric_card(
            "INTERVENTIONS",
            "3",
            "RETRY · WAIT · SWITCH METHOD",
            "tw-positive"
        )


# ============================================================
# DECISION PIPELINE
# ============================================================

def render_decision_pipeline():

    render_html(
        """
        <div style="
            margin-top:3rem;
            margin-bottom:1.2rem;
        ">

            <div class="tw-eyebrow">
                DECISION PIPELINE
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                From payment signal to action.
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
            ">
                The model estimates recovery probability first.
                The decision engine then translates those probabilities
                into an economic recommendation.
            </div>

        </div>
        """
    )

    steps = [
        (
            "01",
            "FAILED PAYMENT",
            "Observed payment details enter the system."
        ),
        (
            "02",
            "PREPROCESSING",
            "Categorical features are encoded for the model."
        ),
        (
            "03",
            "XGBOOST",
            "The recovery model estimates outcome probability."
        ),
        (
            "04",
            "CALIBRATION",
            "Predicted probabilities are calibrated using 5-fold CV."
        ),
        (
            "05",
            "WHAT-IF ANALYSIS",
            "RETRY, WAIT, and SWITCH METHOD are evaluated."
        ),
        (
            "06",
            "ECONOMIC DECISION",
            "Expected recovered value minus action cost determines the recommendation."
        ),
    ]

    for index in range(
        0,
        len(steps),
        3
    ):

        cols = st.columns(
            3,
            gap="medium"
        )

        for col, step in zip(
            cols,
            steps[index:index + 3]
        ):

            number, title, description = step

            with col:

                render_html(
                    f"""
                    <div class="tw-card"
                         style="
                             min-height:165px;
                             position:relative;
                         ">

                        <div style="
                            color:#B0B9BA;
                            font-size:0.68rem;
                            font-weight:750;
                            letter-spacing:0.08em;
                        ">
                            {number}
                        </div>

                        <div style="
                            color:#17252B;
                            font-size:0.92rem;
                            font-weight:750;
                            margin-top:0.65rem;
                            letter-spacing:0.01em;
                        ">
                            {title}
                        </div>

                        <div style="
                            color:#65747A;
                            font-size:0.75rem;
                            line-height:1.5;
                            margin-top:0.5rem;
                        ">
                            {description}
                        </div>

                    </div>
                    """
                )


# ============================================================
# MODEL ARCHITECTURE
# ============================================================

def render_architecture():

    render_html(
        """
        <div style="
            margin-top:3rem;
            margin-bottom:1.2rem;
        ">

            <div class="tw-eyebrow">
                MODEL ARCHITECTURE
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                A calibrated recovery model.
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
            ">
                The trained pipeline combines categorical preprocessing,
                an XGBoost classifier, and probability calibration.
            </div>

        </div>
        """
    )

    left, right = st.columns(
        [1, 1],
        gap="large"
    )

    with left:

        render_html(
            """
            <div class="tw-card"
                 style="
                     min-height:270px;
                 ">

                <div class="tw-eyebrow">
                    PREPROCESSING
                </div>

                <div style="
                    color:#17252B;
                    font-size:1.15rem;
                    font-weight:700;
                    margin-top:0.25rem;
                ">
                    Feature transformation
                </div>

                <div style="
                    color:#65747A;
                    font-size:0.76rem;
                    line-height:1.55;
                    margin-top:0.65rem;
                ">
                    Categorical payment attributes are converted
                    using one-hot encoding while numerical features
                    pass through the preprocessing pipeline.
                </div>

                <div style="
                    display:flex;
                    flex-wrap:wrap;
                    gap:0.45rem;
                    margin-top:1.1rem;
                ">

                    <span class="tw-badge tw-badge-green">
                        PAYMENT METHOD
                    </span>

                    <span class="tw-badge tw-badge-green">
                        BANK
                    </span>

                    <span class="tw-badge tw-badge-green">
                        FAILURE REASON
                    </span>

                    <span class="tw-badge tw-badge-green">
                        INTERVENTION
                    </span>

                    <span class="tw-badge tw-badge-green">
                        AMOUNT
                    </span>

                    <span class="tw-badge tw-badge-green">
                        HOUR
                    </span>

                    <span class="tw-badge tw-badge-green">
                        RESPONSE TIME
                    </span>

                </div>

            </div>
            """
        )

    with right:

        render_html(
            f"""
            <div class="tw-card"
                 style="
                     min-height:270px;
                 ">

                <div class="tw-eyebrow">
                    CLASSIFIER
                </div>

                <div style="
                    color:#17252B;
                    font-size:1.15rem;
                    font-weight:700;
                    margin-top:0.25rem;
                ">
                    {type(get_classifier()).__name__}
                </div>

                <div style="
                    color:#65747A;
                    font-size:0.76rem;
                    line-height:1.55;
                    margin-top:0.65rem;
                ">
                    A gradient-boosted tree classifier learns patterns
                    associated with successful payment recovery.
                    The trained classifier contains 300 estimators
                    with a learning rate of 0.05.
                </div>

                <div style="
                    margin-top:1.15rem;
                    padding-top:0.9rem;
                    border-top:1px solid #DDE3E0;
                ">

                    <div style="
                        color:#65747A;
                        font-size:0.68rem;
                    ">
                        CALIBRATION
                    </div>

                    <div style="
                        color:#167C83;
                        font-size:0.9rem;
                        font-weight:750;
                        margin-top:0.25rem;
                    ">
                        5-FOLD CALIBRATED CLASSIFIER
                    </div>

                </div>

            </div>
            """
        )


# ============================================================
# FEATURE SPACE
# ============================================================

def render_feature_space():

    render_html(
        """
        <div style="
            margin-top:3rem;
            margin-bottom:1.2rem;
        ">

            <div class="tw-eyebrow">
                FEATURE SPACE
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                What the model sees.
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
                max-width:760px;
            ">
                Seven business-level inputs are transformed into
                20 model-ready features through categorical encoding
                and numerical passthrough.
            </div>

        </div>
        """
    )

    categories = [
        (
            "CATEGORICAL",
            "Payment method",
            "3 encoded features"
        ),
        (
            "CATEGORICAL",
            "Bank",
            "5 encoded features"
        ),
        (
            "CATEGORICAL",
            "Failure reason",
            "5 encoded features"
        ),
        (
            "CATEGORICAL",
            "Intervention",
            "4 encoded features"
        ),
        (
            "NUMERICAL",
            "Amount",
            "1 feature"
        ),
        (
            "NUMERICAL",
            "Hour",
            "1 feature"
        ),
        (
            "NUMERICAL",
            "Response time",
            "1 feature"
        ),
    ]

    cols = st.columns(
        4,
        gap="medium"
    )

    for index, (
        category,
        name,
        detail
    ) in enumerate(categories):

        with cols[
            index % 4
        ]:

            render_html(
                f"""
                <div class="tw-card"
                     style="
                         min-height:125px;
                         margin-bottom:0.7rem;
                     ">

                    <div style="
                        color:#167C83;
                        font-size:0.6rem;
                        font-weight:750;
                        letter-spacing:0.08em;
                    ">
                        {category}
                    </div>

                    <div style="
                        color:#17252B;
                        font-size:0.86rem;
                        font-weight:700;
                        margin-top:0.45rem;
                    ">
                        {name}
                    </div>

                    <div style="
                        color:#7D898D;
                        font-size:0.68rem;
                        margin-top:0.3rem;
                    ">
                        {detail}
                    </div>

                </div>
                """
            )


# ============================================================
# DECISION LOGIC
# ============================================================

def render_decision_logic():

    render_html(
        """
        <div style="
            margin-top:3rem;
            margin-bottom:1.2rem;
        ">

            <div class="tw-eyebrow">
                ECONOMIC DECISIONING
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                Probability is not the final decision.
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
            ">
                Payment Twin converts probability into an economic
                decision so the highest-probability action is not
                automatically assumed to be the best action.
            </div>

        </div>
        """
    )

    left, right = st.columns(
        [1.15, 1],
        gap="large"
    )

    with left:

        render_html(
            """
            <div class="tw-card"
                 style="
                     min-height:235px;
                     display:flex;
                     flex-direction:column;
                     justify-content:center;
                 ">

                <div style="
                    color:#7D898D;
                    font-size:0.68rem;
                    font-weight:750;
                    letter-spacing:0.08em;
                ">
                    DECISION FORMULA
                </div>

                <div style="
                    color:#17252B;
                    font-size:1.35rem;
                    font-weight:700;
                    margin-top:0.65rem;
                    letter-spacing:-0.025em;
                ">
                    Expected recovered value
                    <span style="color:#AAB2B3;">
                        −
                    </span>
                    intervention cost
                </div>

                <div style="
                    color:#65747A;
                    font-size:0.76rem;
                    line-height:1.55;
                    margin-top:0.75rem;
                ">
                    For every hypothetical intervention, Payment Twin
                    estimates the amount expected to be recovered and
                    subtracts the simulated cost of taking that action.
                </div>

            </div>
            """
        )

    with right:

        render_html(
            """
            <div class="tw-card"
                 style="
                     min-height:235px;
                 ">

                <div class="tw-eyebrow">
                    THREE-WAY WHAT-IF
                </div>

                <div style="
                    margin-top:0.65rem;
                    display:flex;
                    flex-direction:column;
                    gap:0.6rem;
                ">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        color:#17252B;
                        font-size:0.78rem;
                    ">
                        <span>RETRY</span>
                        <span style="color:#7D898D;">
                            ₹20 simulated cost
                        </span>
                    </div>

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        color:#17252B;
                        font-size:0.78rem;
                    ">
                        <span>WAIT</span>
                        <span style="color:#7D898D;">
                            ₹10 simulated cost
                        </span>
                    </div>

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        color:#17252B;
                        font-size:0.78rem;
                    ">
                        <span>SWITCH METHOD</span>
                        <span style="color:#7D898D;">
                            ₹35 simulated cost
                        </span>
                    </div>

                </div>

                <div style="
                    margin-top:1rem;
                    padding-top:0.85rem;
                    border-top:1px solid #DDE3E0;
                    color:#167C83;
                    font-size:0.7rem;
                    font-weight:750;
                    letter-spacing:0.04em;
                ">
                    HIGHEST ECONOMIC SCORE → RECOMMENDATION
                </div>

            </div>
            """
        )


# ============================================================
# PAGE
# ============================================================

def render_model_intelligence():

    render_page_header()

    render_model_overview()

    render_decision_pipeline()

    render_architecture()

    render_feature_space()

    render_decision_logic()