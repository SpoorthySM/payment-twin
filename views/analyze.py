import streamlit as st
import pandas as pd

from payment_twin import PaymentTwin
from components.styles import render_html


# ============================================================
# MODEL
# ============================================================

@st.cache_resource
def load_payment_twin():
    return PaymentTwin(
        model_path="models/calibrated_model.pkl"
    )


twin = load_payment_twin()


# ============================================================
# HELPERS
# ============================================================

def format_currency(value):
    return f"₹{value:,.0f}"


def format_currency_decimal(value):
    return f"₹{value:,.2f}"


# ============================================================
# PAGE HEADER
# ============================================================

def render_page_header():

    render_html(
        """
        <div class="tw-eyebrow">
            PAYMENT INVESTIGATION
        </div>

        <div class="tw-title">
            Find the right recovery action.
        </div>

        <div class="tw-subtitle">
            Evaluate a failed payment and identify the intervention
            with the highest expected recovery value.
        </div>

        <div class="tw-line"></div>
        """
    )


# ============================================================
# RECOMMENDATION CARD
# ============================================================

def render_recommendation(result):

    action = result["recommended_action"]
    probability = result["predicted_recovery"]
    priority = result["priority"]
    incremental_value = result["expected_incremental_value"]

    render_html(
        f"""
        <div class="recommendation" style="
            min-height:420px;
            display:flex;
            flex-direction:column;
            justify-content:center;
        ">

            <div class="recommendation-label">
                PAYMENT TWIN RECOMMENDATION
            </div>

            <div class="recommendation-action">
                {action}
            </div>

            <div class="recommendation-probability">
                {probability:.1%} predicted recovery
            </div>

            <div style="
                color:#52636A;
                font-size:0.8rem;
                line-height:1.55;
                margin-top:0.9rem;
                max-width:430px;
            ">
                {action.title()} produces the highest
                expected economic value among the
                available recovery strategies.
            </div>

            <div style="
                display:flex;
                gap:0.7rem;
                align-items:center;
                flex-wrap:wrap;
                margin-top:1.3rem;
            ">

                <span class="tw-badge tw-badge-green">
                    {priority} PRIORITY
                </span>

                <span style="
                    color:#65747A;
                    font-size:0.75rem;
                ">
                    Expected value
                    <strong style="color:#17252B;">
                        {format_currency(incremental_value)}
                    </strong>
                </span>

            </div>

            <div style="
                margin-top:2rem;
                padding-top:1.25rem;
                border-top:1px solid #D7E1DD;
                width:100%;
            ">

                <a href="#decision-analysis"
                   style="
                       display:flex;
                       align-items:center;
                       justify-content:space-between;
                       width:100%;
                       color:#4B32C3;
                       text-decoration:none;
                       font-size:1.05rem;
                       font-weight:750;
                       letter-spacing:-0.02em;
                       line-height:1.2;
                   ">

                    <span>
                        Review decision analysis
                    </span>

                    <span style="
                        font-size:1.8rem;
                        font-weight:400;
                        line-height:1;
                        margin-left:1rem;
                    ">
                        ↓
                    </span>

                </a>

                <div style="
                    color:#65747A;
                    font-size:0.75rem;
                    line-height:1.5;
                    margin-top:0.5rem;
                    max-width:400px;
                ">
                    Compare all interventions and inspect
                    the model explanation.
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# DECISION STRENGTH
# ============================================================

def render_decision_strength(result):

    probability_margin = result["probability_margin"]
    economic_margin = result["economic_margin"]
    incremental_value = result["expected_incremental_value"]
    action_cost = result["action_cost"]

    render_html(
        """
        <div class="tw-eyebrow">
            DECISION STRENGTH
        </div>
        """
    )

    cols = st.columns(4, gap="medium")

    with cols[0]:

        render_html(
            f"""
            <div class="tw-card">

                <div class="tw-card-title">
                    Probability margin
                </div>

                <div class="tw-big-number tw-blue">
                    {probability_margin:.2%}
                </div>

                <div style="
                    color:#7D898D;
                    font-size:0.72rem;
                    margin-top:0.6rem;
                ">
                    Gap between the top two actions
                </div>

            </div>
            """
        )

    with cols[1]:

        render_html(
            f"""
            <div class="tw-card">

                <div class="tw-card-title">
                    Economic margin
                </div>

                <div class="tw-big-number tw-positive">
                    {format_currency(economic_margin)}
                </div>

                <div style="
                    color:#7D898D;
                    font-size:0.72rem;
                    margin-top:0.6rem;
                ">
                    Advantage over second-best action
                </div>

            </div>
            """
        )

    with cols[2]:

        render_html(
            f"""
            <div class="tw-card">

                <div class="tw-card-title">
                    Incremental value
                </div>

                <div class="tw-big-number tw-positive">
                    {format_currency(incremental_value)}
                </div>

                <div style="
                    color:#7D898D;
                    font-size:0.72rem;
                    margin-top:0.6rem;
                ">
                    Expected value above baseline
                </div>

            </div>
            """
        )

    with cols[3]:

        render_html(
            f"""
            <div class="tw-card">

                <div class="tw-card-title">
                    Action cost
                </div>

                <div class="tw-big-number">
                    {format_currency(action_cost)}
                </div>

                <div style="
                    color:#7D898D;
                    font-size:0.72rem;
                    margin-top:0.6rem;
                ">
                    Simulated intervention cost
                </div>

            </div>
            """
        )


# ============================================================
# INTERVENTION COMPARISON
# ============================================================

def render_intervention_comparison(result):

    render_html(
        """
        <div style="
            margin-top:2.7rem;
            margin-bottom:1.15rem;
        ">

            <div class="tw-eyebrow">
                INTERVENTION COMPARISON
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                Which action creates the most value?
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
                max-width:720px;
            ">
                Payment Twin compares recovery probability,
                expected recovered value, intervention cost,
                and final decision score.
            </div>

        </div>
        """
    )

    table = result["decision_results"].copy()

    # --------------------------------------------------------
    # Render each intervention as a decision card
    # --------------------------------------------------------

    for _, row in table.iterrows():

        intervention = str(
            row["intervention"]
        )

        action_name = intervention.replace(
            "_",
            " "
        )

        probability = float(
            row["predicted_recovery"]
        )

        recovered_value = float(
            row["expected_recovered_value"]
        )

        action_cost = float(
            row["action_cost"]
        )

        decision_score = float(
            row["decision_score"]
        )

        recommended = (
            intervention
            == result["recommended_action"]
        )

        if recommended:

            background = "#E8F3EE"
            border = "#B9D9CC"
            accent = "#4B9B7B"
            label = "RECOMMENDED"

        else:

            background = "#FFFFFF"
            border = "#DDE3E0"
            accent = "#167C83"
            label = ""

        render_html(
            f"""
            <div style="
                background:{background};
                border:1px solid {border};
                border-radius:12px;
                padding:1.15rem 1.3rem;
                margin-bottom:0.7rem;
            ">

                <div style="
                    display:flex;
                    align-items:center;
                    justify-content:space-between;
                    gap:1rem;
                    margin-bottom:0.9rem;
                ">

                    <div style="
                        color:#17252B;
                        font-size:1rem;
                        font-weight:750;
                        text-transform:uppercase;
                        letter-spacing:0.01em;
                    ">
                        {action_name}
                    </div>

                    {
                        f'''
                        <div style="
                            color:{accent};
                            font-size:0.65rem;
                            font-weight:750;
                            letter-spacing:0.08em;
                        ">
                            ✓ {label}
                        </div>
                        '''
                        if recommended
                        else ""
                    }

                </div>

                <div style="
                    display:grid;
                    grid-template-columns:
                        1fr 1fr 1fr 1fr;
                    gap:1rem;
                ">

                    <div>

                        <div style="
                            color:#899598;
                            font-size:0.62rem;
                            font-weight:700;
                            letter-spacing:0.07em;
                            text-transform:uppercase;
                        ">
                            Recovery
                        </div>

                        <div style="
                            color:#17252B;
                            font-size:1.15rem;
                            font-weight:750;
                            margin-top:0.25rem;
                        ">
                            {probability:.1%}
                        </div>

                    </div>

                    <div>

                        <div style="
                            color:#899598;
                            font-size:0.62rem;
                            font-weight:700;
                            letter-spacing:0.07em;
                            text-transform:uppercase;
                        ">
                            Recovered value
                        </div>

                        <div style="
                            color:#4B9B7B;
                            font-size:1.15rem;
                            font-weight:750;
                            margin-top:0.25rem;
                        ">
                            {format_currency(recovered_value)}
                        </div>

                    </div>

                    <div>

                        <div style="
                            color:#899598;
                            font-size:0.62rem;
                            font-weight:700;
                            letter-spacing:0.07em;
                            text-transform:uppercase;
                        ">
                            Action cost
                        </div>

                        <div style="
                            color:#17252B;
                            font-size:1.15rem;
                            font-weight:750;
                            margin-top:0.25rem;
                        ">
                            {format_currency(action_cost)}
                        </div>

                    </div>

                    <div>

                        <div style="
                            color:#899598;
                            font-size:0.62rem;
                            font-weight:700;
                            letter-spacing:0.07em;
                            text-transform:uppercase;
                        ">
                            Decision score
                        </div>

                        <div style="
                            color:#167C83;
                            font-size:1.15rem;
                            font-weight:750;
                            margin-top:0.25rem;
                        ">
                            {format_currency(decision_score)}
                        </div>

                    </div>

                </div>

            </div>
            """
        )


# ============================================================
# MODEL EXPLANATION
# ============================================================

def render_explanation(result):

    explanation = result.get(
        "explanation",
        None
    )

    render_html(
        """
        <div style="
            margin-top:2.8rem;
            margin-bottom:1.15rem;
        ">

            <div class="tw-eyebrow">
                MODEL EXPLANATION
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                Why did Payment Twin choose this?
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
                max-width:720px;
            ">
                The strongest model signals influencing the
                recovery prediction.
            </div>

        </div>
        """
    )

    if explanation is None:

        render_html(
            """
            <div class="tw-card">

                <div style="
                    color:#65747A;
                    font-size:0.8rem;
                ">
                    Model explanation is unavailable for this payment.
                </div>

            </div>
            """
        )

        return

    # --------------------------------------------------------
    # DataFrame explanation
    # --------------------------------------------------------

    if isinstance(
        explanation,
        pd.DataFrame
    ):

        exp = explanation.copy()

        if "human_feature" in exp.columns:

            feature_column = "human_feature"

        elif "feature" in exp.columns:

            feature_column = "feature"

        else:

            feature_column = exp.columns[0]

        if "shap_value" in exp.columns:

            value_column = "shap_value"

        else:

            value_column = exp.columns[1]

        exp = exp[
            [
                feature_column,
                value_column
            ]
        ].copy()

        exp.columns = [
            "Signal",
            "Contribution"
        ]

        exp["Contribution"] = pd.to_numeric(
            exp["Contribution"],
            errors="coerce"
        )

        exp = exp.dropna(
            subset=["Contribution"]
        )

        # Show strongest signals first
        exp["magnitude"] = exp[
            "Contribution"
        ].abs()

        exp = exp.sort_values(
            "magnitude",
            ascending=False
        ).head(6)

        max_value = max(
            exp["magnitude"].max(),
            0.0001
        )

        for _, row in exp.iterrows():

            signal = str(
                row["Signal"]
            )

            contribution = float(
                row["Contribution"]
            )

            magnitude = abs(
                contribution
            )

            width = (
                magnitude / max_value
            ) * 100

            if contribution >= 0:

                bar_color = "#4B9B7B"
                direction = "↑"
                direction_color = "#4B9B7B"

            else:

                bar_color = "#C7796B"
                direction = "↓"
                direction_color = "#C7796B"

            render_html(
                f"""
                <div style="
                    background:#FFFFFF;
                    border:1px solid #DDE3E0;
                    border-radius:10px;
                    padding:0.95rem 1.15rem;
                    margin-bottom:0.6rem;
                ">

                    <div style="
                        display:flex;
                        align-items:center;
                        justify-content:space-between;
                        gap:1rem;
                    ">

                        <div style="
                            color:#17252B;
                            font-size:0.8rem;
                            font-weight:650;
                        ">
                            {signal}
                        </div>

                        <div style="
                            color:{direction_color};
                            font-size:0.82rem;
                            font-weight:750;
                            white-space:nowrap;
                        ">
                            {direction}
                            {contribution:+.3f}
                        </div>

                    </div>

                    <div style="
                        margin-top:0.65rem;
                        height:5px;
                        background:#E9EEEB;
                        border-radius:10px;
                        overflow:hidden;
                    ">

                        <div style="
                            width:{width:.1f}%;
                            height:100%;
                            background:{bar_color};
                            border-radius:10px;
                        "></div>

                    </div>

                </div>
                """
            )

    else:

        render_html(
            f"""
            <div class="tw-card">

                <div style="
                    color:#52636A;
                    font-size:0.8rem;
                    line-height:1.55;
                ">
                    {explanation}
                </div>

            </div>
            """
        )


# ============================================================
# PAYMENT INPUTS
# ============================================================

def render_input_card():

    render_html(
        """
        <div style="
            margin-bottom:1.15rem;
        ">

            <div class="tw-eyebrow">
                PAYMENT DETAILS
            </div>

            <div style="
                color:#17252B;
                font-size:1.55rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                What happened?
            </div>

            <div style="
                color:#65747A;
                font-size:0.8rem;
                margin-top:0.35rem;
            ">
                Provide the observed details of the failed payment.
            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # Default example payment
    # --------------------------------------------------------

    default_amount = 27320
    default_method = "CARD"
    default_bank = "KOTAK"
    default_hour = 11
    default_response = 19.3
    default_reason = "TIMEOUT"

    # --------------------------------------------------------
    # Amount
    # --------------------------------------------------------

    amount = st.number_input(
        "Amount (₹)",
        min_value=1,
        value=default_amount,
        step=100
    )

    # --------------------------------------------------------
    # Method + bank
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        payment_method = st.selectbox(
            "Payment Method",
            [
                "UPI",
                "CARD",
                "NET_BANKING"
            ],
            index=[
                "UPI",
                "CARD",
                "NET_BANKING"
            ].index(default_method)
        )

    with col2:

        bank = st.selectbox(
            "Bank",
            [
                "AXIS",
                "HDFC",
                "ICICI",
                "KOTAK",
                "SBI"
            ],
            index=[
                "AXIS",
                "HDFC",
                "ICICI",
                "KOTAK",
                "SBI"
            ].index(default_bank)
        )

    # --------------------------------------------------------
    # Hour + response time
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        hour = st.number_input(
            "Hour",
            min_value=0,
            max_value=23,
            value=default_hour,
            step=1
        )

    with col2:

        response_time = st.number_input(
            "Response Time (seconds)",
            min_value=0.0,
            value=default_response,
            step=0.1
        )

    # --------------------------------------------------------
    # Failure reason
    # --------------------------------------------------------

    failure_reason = st.selectbox(
        "Failure Reason",
        [
            "TIMEOUT",
            "AUTHENTICATION_FAILED",
            "BANK_ERROR",
            "INSUFFICIENT_FUNDS",
            "USER_CANCELLED"
        ],
        index=[
            "TIMEOUT",
            "AUTHENTICATION_FAILED",
            "BANK_ERROR",
            "INSUFFICIENT_FUNDS",
            "USER_CANCELLED"
        ].index(default_reason)
    )

    st.markdown(
        "<div style='height:0.5rem'></div>",
        unsafe_allow_html=True
    )

    analyze = st.button(
        "Analyze payment  →",
        type="primary",
        use_container_width=True
    )

    return (
        analyze,
        amount,
        payment_method,
        bank,
        hour,
        response_time,
        failure_reason
    )


# ============================================================
# PAGE
# ============================================================

def render_analyze():

    render_page_header()

    # --------------------------------------------------------
    # Top workspace
    # --------------------------------------------------------

    left, right = st.columns(
        [1, 1.15],
        gap="large"
    )

    # --------------------------------------------------------
    # LEFT — PAYMENT INPUT
    # --------------------------------------------------------

    with left:

        (
            analyze,
            amount,
            payment_method,
            bank,
            hour,
            response_time,
            failure_reason
        ) = render_input_card()

    # --------------------------------------------------------
    # RIGHT — READY / RECOMMENDATION
    # --------------------------------------------------------

    with right:

        if "analysis_result" not in st.session_state:

            render_html(
                """
                <div class="tw-card" style="
                    min-height:420px;
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    align-items:flex-start;
                ">

                    <div class="tw-eyebrow">
                        PAYMENT TWIN
                    </div>

                    <div style="
                        color:#17252B;
                        font-size:1.8rem;
                        font-weight:650;
                        letter-spacing:-0.045em;
                        line-height:1.1;
                    ">
                        Ready to analyze.
                    </div>

                    <div style="
                        color:#65747A;
                        font-size:0.8rem;
                        line-height:1.55;
                        max-width:420px;
                        margin-top:0.8rem;
                    ">
                        Payment Twin will compare RETRY, WAIT,
                        and SWITCH METHOD, then select the action
                        with the highest expected economic value.
                    </div>

                    <div style="
                        margin-top:1.3rem;
                        padding:0.7rem 0.85rem;
                        background:#EEF3F0;
                        border-radius:8px;
                        color:#52636A;
                        font-size:0.7rem;
                    ">
                        MODEL · DECISION ENGINE · PRIORITIZATION · SHAP
                    </div>

                </div>
                """
            )

        else:

            result = st.session_state.analysis_result

            render_recommendation(result)

    # --------------------------------------------------------
    # RUN ANALYSIS
    # --------------------------------------------------------

    if analyze:

        payment = pd.DataFrame(
            [
                {
                    "payment_id": "DEMO001",
                    "amount": amount,
                    "payment_method": payment_method,
                    "bank": bank,
                    "hour": hour,
                    "response_time": response_time,
                    "failure_reason": failure_reason,
                    "intervention": "WAIT"
                }
            ]
        )

        with st.spinner(
            "Payment Twin is evaluating recovery strategies..."
        ):

            result = twin.analyze(payment)

        st.session_state.analysis_result = result

        st.rerun()

    # --------------------------------------------------------
    # DECISION ANALYSIS LINK + RESULTS
    # --------------------------------------------------------

    if "analysis_result" in st.session_state:

        result = st.session_state.analysis_result

        render_html(
            """
            <div id="decision-analysis"
                 style="
                     height:1px;
                     margin-top:0.4rem;
                 ">
            </div>
            """
        )

        render_decision_strength(result)

        render_intervention_comparison(result)

        render_explanation(result)

        # ----------------------------------------------------
        # RESET
        # ----------------------------------------------------

        st.markdown(
            "<div style='height:2rem'></div>",
            unsafe_allow_html=True
        )

        if st.button(
            "Analyze another payment"
        ):

            del st.session_state.analysis_result

            st.rerun()