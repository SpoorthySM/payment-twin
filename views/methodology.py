import streamlit as st

from components.styles import render_html


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
                METHODOLOGY
            </div>

            <div class="tw-title">
                How Payment Twin
                makes a recovery decision.
            </div>

            <div class="tw-subtitle">
                From failed payment signals to intervention
                prioritization, Payment Twin combines machine
                learning with economic decisioning.
            </div>

            <div class="tw-line"></div>

        </div>
        """
    )


# ============================================================
# SYSTEM FLOW
# ============================================================

def render_system_flow():

    render_html(
        """
        <div style="
            margin-bottom:1.2rem;
        ">

            <div class="tw-eyebrow">
                END-TO-END FRAMEWORK
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                From failed payment to recovery action.
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
            ">
                Each stage contributes to the final recommendation
                and determines where intervention capacity should
                be directed.
            </div>

        </div>
        """
    )

    steps = [
        (
            "01",
            "PAYMENT INPUT",
            "Amount, payment method, bank, hour, response time, and failure reason."
        ),
        (
            "02",
            "VALIDATION",
            "Input values are checked against the expected payment schema."
        ),
        (
            "03",
            "RECOVERY MODEL",
            "The trained XGBoost model estimates recovery probability."
        ),
        (
            "04",
            "CALIBRATION",
            "Probability estimates are calibrated using cross-validation."
        ),
        (
            "05",
            "INTERVENTION SIMULATION",
            "RETRY, WAIT, and SWITCH METHOD are evaluated under the same payment conditions."
        ),
        (
            "06",
            "ECONOMIC DECISION",
            "Expected recovered value is adjusted for intervention cost."
        ),
        (
            "07",
            "PRIORITIZATION",
            "Payments are ranked so limited intervention capacity reaches the strongest opportunities."
        ),
        (
            "08",
            "EXPLANATION",
            "Model signals are surfaced to help explain the prediction."
        ),
    ]

    for start in range(0, len(steps), 4):

        cols = st.columns(
            4,
            gap="medium"
        )

        for col, step in zip(
            cols,
            steps[start:start + 4]
        ):

            number, title, description = step

            with col:

                render_html(
                    f"""
                    <div class="tw-card"
                         style="
                             min-height:175px;
                             margin-bottom:0.8rem;
                         ">

                        <div style="
                            color:#AAB3B5;
                            font-size:0.68rem;
                            font-weight:750;
                            letter-spacing:0.08em;
                        ">
                            {number}
                        </div>

                        <div style="
                            color:#17252B;
                            font-size:0.9rem;
                            font-weight:750;
                            margin-top:0.6rem;
                        ">
                            {title}
                        </div>

                        <div style="
                            color:#65747A;
                            font-size:0.73rem;
                            line-height:1.5;
                            margin-top:0.55rem;
                        ">
                            {description}
                        </div>

                    </div>
                    """
                )


# ============================================================
# PROBLEM → APPROACH
# ============================================================

def render_problem_approach():

    render_html(
        """
        <div style="
            margin-top:3rem;
            margin-bottom:1.2rem;
        ">

            <div class="tw-eyebrow">
                CORE APPROACH
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                The problem is not just prediction.
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
            ">
                A useful recovery system must answer both
                whether a payment can recover and what should
                be done about it.
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
                     min-height:235px;
                 ">

                <div class="tw-eyebrow">
                    PREDICTION
                </div>

                <div style="
                    color:#17252B;
                    font-size:1.25rem;
                    font-weight:700;
                    margin-top:0.25rem;
                ">
                    Can this payment recover?
                </div>

                <div style="
                    color:#65747A;
                    font-size:0.76rem;
                    line-height:1.55;
                    margin-top:0.65rem;
                ">
                    The recovery model uses the observed payment
                    characteristics and a hypothetical intervention
                    to estimate the probability of successful recovery.
                </div>

                <div style="
                    margin-top:1rem;
                    padding-top:0.85rem;
                    border-top:1px solid #DDE3E0;
                    color:#167C83;
                    font-size:0.7rem;
                    font-weight:750;
                    letter-spacing:0.05em;
                ">
                    OUTPUT · RECOVERY PROBABILITY
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
                    DECISION
                </div>

                <div style="
                    color:#17252B;
                    font-size:1.25rem;
                    font-weight:700;
                    margin-top:0.25rem;
                ">
                    What action creates the most value?
                </div>

                <div style="
                    color:#65747A;
                    font-size:0.76rem;
                    line-height:1.55;
                    margin-top:0.65rem;
                ">
                    Payment Twin evaluates each available intervention
                    and selects the action with the highest expected
                    economic value rather than simply choosing the
                    highest probability.
                </div>

                <div style="
                    margin-top:1rem;
                    padding-top:0.85rem;
                    border-top:1px solid #DDE3E0;
                    color:#167C83;
                    font-size:0.7rem;
                    font-weight:750;
                    letter-spacing:0.05em;
                ">
                    OUTPUT · RECOMMENDED INTERVENTION
                </div>

            </div>
            """
        )


# ============================================================
# MODELING
# ============================================================

def render_modeling():

    render_html(
        """
        <div style="
            margin-top:3rem;
            margin-bottom:1.2rem;
        ">

            <div class="tw-eyebrow">
                MODELING
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                Learning recovery patterns from payment data.
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
            ">
                The trained pipeline uses structured payment features
                to estimate the likelihood of recovery for each
                hypothetical intervention.
            </div>

        </div>
        """
    )

    cols = st.columns(
        3,
        gap="medium"
    )

    cards = [
        (
            "FEATURES",
            "Structured payment signals",
            "Categorical attributes such as bank, payment method, failure reason, and intervention are encoded for the model. Numerical attributes pass through the preprocessing pipeline."
        ),
        (
            "CLASSIFIER",
            "XGBoost",
            "A gradient-boosted tree classifier models nonlinear relationships between payment characteristics and recovery outcomes."
        ),
        (
            "CALIBRATION",
            "Calibrated probabilities",
            "The classifier is wrapped with 5-fold probability calibration so its recovery estimates can be interpreted as probabilities rather than raw model scores."
        ),
    ]

    for col, (
        eyebrow,
        title,
        description
    ) in zip(cols, cards):

        with col:

            render_html(
                f"""
                <div class="tw-card"
                     style="
                         min-height:255px;
                     ">

                    <div class="tw-eyebrow">
                        {eyebrow}
                    </div>

                    <div style="
                        color:#17252B;
                        font-size:1.15rem;
                        font-weight:700;
                        margin-top:0.25rem;
                    ">
                        {title}
                    </div>

                    <div style="
                        color:#65747A;
                        font-size:0.76rem;
                        line-height:1.55;
                        margin-top:0.65rem;
                    ">
                        {description}
                    </div>

                </div>
                """
            )


# ============================================================
# ECONOMIC DECISION
# ============================================================

def render_economic_decision():

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
                Turning probability into business value.
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
            ">
                The decision engine evaluates every intervention
                using expected recovered value and simulated
                intervention cost.
            </div>

        </div>
        """
    )

    render_html(
        """
        <div class="tw-card"
             style="
                 min-height:210px;
                 display:flex;
                 flex-direction:column;
                 justify-content:center;
             ">

            <div class="tw-eyebrow">
                DECISION SCORE
            </div>

            <div style="
                color:#17252B;
                font-size:1.5rem;
                font-weight:700;
                letter-spacing:-0.025em;
                margin-top:0.4rem;
            ">
                Expected recovered value
                <span style="color:#AAB3B5;">
                    −
                </span>
                intervention cost
            </div>

            <div style="
                color:#65747A;
                font-size:0.78rem;
                line-height:1.55;
                margin-top:0.7rem;
                max-width:780px;
            ">
                For each hypothetical intervention, the predicted
                recovery probability is multiplied by the payment
                amount to estimate expected recovered value. The
                simulated action cost is then subtracted to produce
                the economic decision score.
            </div>

        </div>
        """
    )

    st.markdown(
        "<div style='height:0.9rem'></div>",
        unsafe_allow_html=True
    )

    cols = st.columns(
        3,
        gap="medium"
    )

    actions = [
        (
            "RETRY",
            "₹20",
            "Simulated intervention cost"
        ),
        (
            "WAIT",
            "₹10",
            "Simulated intervention cost"
        ),
        (
            "SWITCH METHOD",
            "₹35",
            "Simulated intervention cost"
        ),
    ]

    for col, (
        action,
        cost,
        description
    ) in zip(cols, actions):

        with col:

            render_html(
                f"""
                <div class="tw-card"
                     style="
                         min-height:125px;
                     ">

                    <div style="
                        color:#167C83;
                        font-size:0.72rem;
                        font-weight:750;
                        letter-spacing:0.05em;
                    ">
                        {action}
                    </div>

                    <div style="
                        color:#17252B;
                        font-size:1.25rem;
                        font-weight:700;
                        margin-top:0.45rem;
                    ">
                        {cost}
                    </div>

                    <div style="
                        color:#7D898D;
                        font-size:0.68rem;
                        margin-top:0.25rem;
                    ">
                        {description}
                    </div>

                </div>
                """
            )


# ============================================================
# PRIORITIZATION
# ============================================================

def render_prioritization():

    render_html(
        """
        <div style="
            margin-top:3rem;
            margin-bottom:1.2rem;
        ">

            <div class="tw-eyebrow">
                PRIORITIZATION
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                From individual decisions to an action queue.
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
            ">
                When intervention capacity is limited, payments are
                ordered by priority first and expected incremental
                value second.
            </div>

        </div>
        """
    )

    render_html(
        """
        <div class="tw-card"
             style="
                 min-height:175px;
             ">

            <div style="
                display:flex;
                flex-wrap:wrap;
                align-items:center;
                justify-content:center;
                gap:0.65rem;
                color:#17252B;
                font-size:0.85rem;
                font-weight:700;
                text-align:center;
            ">

                <span>
                    FAILED PAYMENTS
                </span>

                <span style="color:#167C83;">
                    →
                </span>

                <span>
                    PRIORITY
                </span>

                <span style="color:#167C83;">
                    →
                </span>

                <span>
                    EXPECTED VALUE
                </span>

                <span style="color:#167C83;">
                    →
                </span>

                <span>
                    RECOVERY QUEUE
                </span>

            </div>

            <div style="
                color:#65747A;
                font-size:0.76rem;
                line-height:1.55;
                text-align:center;
                max-width:850px;
                margin:1rem auto 0 auto;
            ">
                This allows the system to translate model predictions
                into an operational recommendation: if only a fraction
                of failed payments can be handled, act on the strongest
                opportunities first.
            </div>

        </div>
        """
    )


# ============================================================
# EXPLAINABILITY
# ============================================================

def render_explainability():

    render_html(
        """
        <div style="
            margin-top:3rem;
            margin-bottom:1.2rem;
        ">

            <div class="tw-eyebrow">
                EXPLAINABILITY
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                Making the prediction inspectable.
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
            ">
                Payment Twin surfaces the strongest model signals
                influencing the recovery prediction so that a
                recommendation is not treated as a black box.
            </div>

        </div>
        """
    )

    cols = st.columns(
        3,
        gap="medium"
    )

    items = [
        (
            "PREDICTION",
            "Recovery probability",
            "Estimated likelihood of successful recovery."
        ),
        (
            "SIGNALS",
            "Model contribution",
            "Features associated with the model's prediction."
        ),
        (
            "DECISION",
            "Recommended action",
            "Economic comparison determines the final intervention."
        ),
    ]

    for col, (
        eyebrow,
        title,
        description
    ) in zip(cols, items):

        with col:

            render_html(
                f"""
                <div class="tw-card"
                     style="
                         min-height:155px;
                     ">

                    <div class="tw-eyebrow">
                        {eyebrow}
                    </div>

                    <div style="
                        color:#17252B;
                        font-size:1rem;
                        font-weight:700;
                        margin-top:0.25rem;
                    ">
                        {title}
                    </div>

                    <div style="
                        color:#65747A;
                        font-size:0.73rem;
                        line-height:1.5;
                        margin-top:0.5rem;
                    ">
                        {description}
                    </div>

                </div>
                """
            )


# ============================================================
# PAGE
# ============================================================

def render_methodology():

    render_page_header()

    render_system_flow()

    render_problem_approach()

    render_modeling()

    render_economic_decision()

    render_prioritization()

    render_explainability()