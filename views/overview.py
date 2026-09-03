import streamlit as st

from components.styles import render_html
from components.metrics import (
    metric_block,
    section_header
)

from components.charts import (
    recovery_capacity_chart,
    lift_chart
)


def render_overview():

    # ========================================================
    # HERO
    # ========================================================

    render_html(
        """
<div style="
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
">

    <div class="tw-eyebrow">
        PAYMENT RECOVERY INTELLIGENCE
    </div>

    <div class="tw-title">
        Turn failed payments<br>
        into recoverable opportunities.
    </div>

    <div class="tw-subtitle">
        Payment Twin predicts recovery, evaluates intervention
        strategies, and identifies the payments where action
        has the greatest expected value.
    </div>

</div>

<div class="tw-line"></div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # KPI STRIP
    # ========================================================

    cols = st.columns(
        4,
        gap="medium"
    )

    with cols[0]:
        metric_block(
            "Failed payments",
            "45,993",
            "Observed failed transactions",
            "blue"
        )

    with cols[1]:
        metric_block(
            "Observed recovery",
            "35.59%",
            "Historical recovery rate",
            "positive"
        )

    with cols[2]:
        metric_block(
            "Top-10% recovery",
            "56.47%",
            "Recovery among highest-ranked payments",
            "positive"
        )

    with cols[3]:
        metric_block(
            "Top-10% lift",
            "1.59×",
            "Versus overall recovery",
            "blue"
        )


    render_html(
        "<div style='height:0.8rem'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # PERFORMANCE SECTION
    # ========================================================

    section_header(
        "RECOVERY PERFORMANCE",
        "Recovery is concentrated.",
        "The Twin's ranking allows intervention capacity to be "
        "focused on payments with substantially higher recovery "
        "potential."
    )

    left, right = st.columns(
        [1.35, 1],
        gap="large"
    )


    # --------------------------------------------------------
    # Capacity chart
    # --------------------------------------------------------

    with left:

        render_html(
            """
<div class="tw-card">

    <div class="tw-card-title">
        Recovery by intervention capacity
    </div>

    <div style="
        color:#17252B;
        font-size:1.15rem;
        font-weight:650;
        letter-spacing:-0.025em;
        margin-bottom:0.15rem;
    ">
        Prioritize the highest-value failures first.
    </div>

    <div style="
        color:#7D898D;
        font-size:0.76rem;
        line-height:1.5;
        margin-bottom:0.5rem;
    ">
        Observed recovery among the highest-ranked payments.
    </div>
            """,
            unsafe_allow_html=True
        )

        recovery_capacity_chart()

        render_html(
            """
    <div style="
        border-top:1px solid #DDE2DF;
        padding-top:0.8rem;
        color:#65747A;
        font-size:0.74rem;
        line-height:1.5;
    ">
        At <strong style="color:#287C83;">10% capacity</strong>,
        the ranked pool reaches
        <strong style="color:#4E9278;">56.47%</strong> recovery
        versus <strong>35.59%</strong> overall.
    </div>

</div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # Lift chart
    # --------------------------------------------------------

    with right:

        render_html(
            """
<div class="tw-card">

    <div class="tw-card-title">
        Ranking lift
    </div>

    <div style="
        color:#17252B;
        font-size:1.15rem;
        font-weight:650;
        letter-spacing:-0.025em;
        margin-bottom:0.15rem;
    ">
        The ranking changes who gets attention.
    </div>

    <div style="
        color:#7D898D;
        font-size:0.76rem;
        line-height:1.5;
        margin-bottom:0.5rem;
    ">
        Recovery lift relative to the overall population.
    </div>
            """,
            unsafe_allow_html=True
        )

        lift_chart()

        render_html(
            """
    <div style="
        border-top:1px solid #DDE2DF;
        padding-top:0.8rem;
        color:#65747A;
        font-size:0.74rem;
        line-height:1.5;
    ">
        The top 10% of ranked payments recover at
        <strong style="color:#287C83;">1.59×</strong>
        the overall recovery rate.
    </div>

</div>
            """,
            unsafe_allow_html=True
        )


    render_html(
        "<div style='height:2.8rem'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # DECISION PIPELINE
    # ========================================================

    section_header(
        "DECISION PIPELINE",
        "From payment failure to action.",
        "Prediction is only the first layer. Payment Twin combines "
        "recovery modelling, intervention comparison, economic "
        "value, prioritization, and explainability."
    )

    steps = st.columns(
        5,
        gap="small"
    )

    pipeline = [
        (
            "01",
            "PREDICT",
            "Estimate the probability that a failed payment can recover."
        ),
        (
            "02",
            "SIMULATE",
            "Evaluate RETRY, WAIT, and SWITCH_METHOD."
        ),
        (
            "03",
            "VALUE",
            "Account for payment amount and intervention cost."
        ),
        (
            "04",
            "PRIORITIZE",
            "Surface the opportunities with the greatest expected value."
        ),
        (
            "05",
            "EXPLAIN",
            "Expose the strongest model signals behind the decision."
        )
    ]

    for column, step in zip(
        steps,
        pipeline
    ):

        with column:

            render_html(
                f"""
<div class="tw-card" style="height:100%;">

    <div style="
        color:#287C83;
        font-size:0.67rem;
        font-weight:750;
        letter-spacing:0.1em;
        margin-bottom:1.25rem;
    ">
        {step[0]}
    </div>

    <div style="
        color:#17252B;
        font-size:0.78rem;
        font-weight:750;
        letter-spacing:0.09em;
    ">
        {step[1]}
    </div>

    <div style="
        color:#7D898D;
        font-size:0.74rem;
        line-height:1.55;
        margin-top:0.65rem;
    ">
        {step[2]}
    </div>

</div>
                """,
                unsafe_allow_html=True
            )


    render_html(
        "<div style='height:2.8rem'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # EVALUATION NOTE
    # ========================================================

    render_html(
        """
<div style="
    background:#EEF3F0;
    border:1px solid #D7E2DD;
    border-radius:12px;
    padding:1.2rem 1.4rem;
">

    <div style="
        color:#287C83;
        font-size:0.67rem;
        font-weight:750;
        letter-spacing:0.12em;
        text-transform:uppercase;
        margin-bottom:0.45rem;
    ">
        Evaluation note
    </div>

    <div style="
        color:#52636A;
        font-size:0.76rem;
        line-height:1.6;
        max-width:950px;
    ">
        Offline policy evaluation did not establish a meaningful
        advantage over the historical intervention policy.
        Payment Twin therefore focuses on prediction,
        prioritization, economic decision support, and
        explainability rather than claiming autonomous causal
        optimization.
    </div>

</div>
        """,
        unsafe_allow_html=True
    )