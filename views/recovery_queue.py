import streamlit as st
import pandas as pd

from payment_twin import PaymentTwin
from portfolio import (
    build_recovery_queue,
    evaluate_capacity,
    summarize_queue,
)
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


def priority_color(priority):
    if priority == "HIGH":
        return "#2F8F70"

    if priority == "MEDIUM":
        return "#B47A2C"

    return "#7D898D"


def priority_background(priority):
    if priority == "HIGH":
        return "#E8F3EE"

    if priority == "MEDIUM":
        return "#F5EFE3"

    return "#EEF1F0"


# ============================================================
# DEMO PORTFOLIO
# ============================================================

def build_demo_portfolio():

    payments = pd.DataFrame(
        [
            {
                "payment_id": "P001",
                "amount": 50000,
                "payment_method": "CARD",
                "bank": "KOTAK",
                "hour": 11,
                "response_time": 19.3,
                "failure_reason": "TIMEOUT",
                "intervention": "WAIT",
            },
            {
                "payment_id": "P002",
                "amount": 30000,
                "payment_method": "UPI",
                "bank": "HDFC",
                "hour": 14,
                "response_time": 8.4,
                "failure_reason": "BANK_ERROR",
                "intervention": "WAIT",
            },
            {
                "payment_id": "P003",
                "amount": 10000,
                "payment_method": "CARD",
                "bank": "SBI",
                "hour": 19,
                "response_time": 4.8,
                "failure_reason": "USER_CANCELLED",
                "intervention": "WAIT",
            },
        ]
    )

    decisions = []

    for _, payment in payments.iterrows():

        payment_df = pd.DataFrame(
            [payment.to_dict()]
        )

        result = twin.analyze(payment_df)

        decisions.append(
            {
                "payment_id": result["payment_id"],
                "amount": float(payment["amount"]),
                "recommended_action": result[
                    "recommended_action"
                ],
                "predicted_recovery": result[
                    "predicted_recovery"
                ],
                "expected_incremental_value": result[
                    "expected_incremental_value"
                ],
                "priority": result["priority"],
            }
        )

    return pd.DataFrame(decisions)


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
                RECOVERY OPERATIONS
            </div>

            <div class="tw-title">
                Recover the highest-value
                payments first.
            </div>

            <div class="tw-subtitle">
                Payment Twin ranks failed payments by recovery potential,
                intervention priority, and expected economic value.
            </div>

            <div class="tw-line"></div>

        </div>
        """
    )


# ============================================================
# SUMMARY
# ============================================================

def render_summary(queue, summary):

    top_payment = queue.iloc[0]

    top_value = top_payment[
        "expected_incremental_value"
    ]

    high_priority = int(
        (queue["priority"] == "HIGH").sum()
    )

    cards = [
        (
            "PAYMENTS IN QUEUE",
            f"{summary['payments']:,}",
            "Failed payments evaluated",
            "tw-blue",
        ),
        (
            "EXPECTED VALUE",
            format_currency(
                summary["total_expected_value"]
            ),
            "Total incremental recovery value",
            "tw-positive",
        ),
        (
            "TOP OPPORTUNITY",
            format_currency(top_value),
            f"{top_payment['payment_id']} · ranked #1",
            "tw-positive",
        ),
        (
            "HIGH PRIORITY",
            f"{high_priority}",
            "Payments requiring highest urgency",
            "tw-blue",
        ),
    ]

    cols = st.columns(
        4,
        gap="medium"
    )

    for col, (
        label,
        value,
        description,
        number_class
    ) in zip(cols, cards):

        with col:

            render_html(
                f"""
                <div class="tw-card"
                     style="
                         min-height:150px;
                         display:flex;
                         flex-direction:column;
                         justify-content:flex-start;
                     ">

                    <div class="tw-card-title">
                        {label}
                    </div>

                    <div class="tw-big-number {number_class}">
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
# QUEUE HEADER
# ============================================================

def render_queue_header():

    render_html(
        """
        <div style="
            margin-top:3rem;
            margin-bottom:1.25rem;
        ">

            <div class="tw-eyebrow">
                RECOVERY QUEUE
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                Where should the team act first?
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
                max-width:760px;
            ">
                Payments are ranked by priority first and expected
                incremental value second, directing limited intervention
                capacity toward the strongest opportunities.
            </div>

        </div>
        """
    )


# ============================================================
# QUEUE ROW
# ============================================================

def render_queue_row(row):

    rank = int(row["rank"])
    payment_id = row["payment_id"]
    amount = row["amount"]
    action = str(
        row["recommended_action"]
    ).replace(
        "_",
        " "
    )
    recovery = row["predicted_recovery"]
    expected_value = row[
        "expected_incremental_value"
    ]
    priority = row["priority"]

    p_color = priority_color(priority)
    p_background = priority_background(priority)

    render_html(
        f"""
        <div style="
            display:grid;
            grid-template-columns:
                55px
                1.15fr
                1fr
                1.45fr
                0.9fr
                1.2fr;
            align-items:center;
            gap:1rem;
            padding:1.15rem 1.35rem;
            background:#FFFFFF;
            border:1px solid #DDE3E0;
            border-radius:12px;
            margin-bottom:0.65rem;
            box-shadow:0 4px 16px rgba(23,37,43,0.035);
        ">

            <div style="
                color:#9AA4A7;
                font-size:0.78rem;
                font-weight:700;
                letter-spacing:0.02em;
            ">
                {rank:02d}
            </div>

            <div>

                <div style="
                    color:#17252B;
                    font-size:0.9rem;
                    font-weight:700;
                ">
                    {payment_id}
                </div>

                <div style="
                    color:#8A969A;
                    font-size:0.68rem;
                    margin-top:0.2rem;
                ">
                    FAILED PAYMENT
                </div>

            </div>

            <div>

                <div style="
                    color:#17252B;
                    font-size:0.9rem;
                    font-weight:650;
                ">
                    {format_currency(amount)}
                </div>

                <div style="
                    color:#8A969A;
                    font-size:0.68rem;
                    margin-top:0.2rem;
                ">
                    PAYMENT AMOUNT
                </div>

            </div>

            <div>

                <div style="
                    color:#167C83;
                    font-size:0.84rem;
                    font-weight:750;
                    text-transform:uppercase;
                ">
                    {action}
                </div>

                <div style="
                    display:inline-block;
                    margin-top:0.35rem;
                    padding:0.2rem 0.5rem;
                    border-radius:20px;
                    background:{p_background};
                    color:{p_color};
                    font-size:0.61rem;
                    font-weight:750;
                    letter-spacing:0.05em;
                ">
                    {priority} PRIORITY
                </div>

            </div>

            <div>

                <div style="
                    color:#17252B;
                    font-size:0.95rem;
                    font-weight:700;
                ">
                    {recovery:.1%}
                </div>

                <div style="
                    color:#8A969A;
                    font-size:0.68rem;
                    margin-top:0.2rem;
                ">
                    RECOVERY
                </div>

            </div>

            <div>

                <div style="
                    color:#4B9B7B;
                    font-size:1.05rem;
                    font-weight:750;
                    letter-spacing:-0.02em;
                ">
                    {format_currency(expected_value)}
                </div>

                <div style="
                    color:#8A969A;
                    font-size:0.68rem;
                    margin-top:0.2rem;
                ">
                    EXPECTED VALUE
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# RECOVERY QUEUE
# ============================================================

def render_queue(queue):

    render_queue_header()

    # Column headings
    render_html(
        """
        <div style="
            display:grid;
            grid-template-columns:
                55px
                1.15fr
                1fr
                1.45fr
                0.9fr
                1.2fr;
            gap:1rem;
            padding:0 1.35rem 0.55rem 1.35rem;
            color:#8A969A;
            font-size:0.63rem;
            font-weight:750;
            letter-spacing:0.09em;
            text-transform:uppercase;
        ">

            <div>#</div>
            <div>Payment</div>
            <div>Amount</div>
            <div>Recovery action</div>
            <div>Probability</div>
            <div>Expected value</div>

        </div>
        """
    )

    for _, row in queue.iterrows():
        render_queue_row(row)


# ============================================================
# CAPACITY PLANNING
# ============================================================

def render_capacity(queue):

    render_html(
        """
        <div style="
            margin-top:3.2rem;
            margin-bottom:1.2rem;
        ">

            <div class="tw-eyebrow">
                CAPACITY PLANNING
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:650;
                letter-spacing:-0.04em;
            ">
                What if intervention capacity is limited?
            </div>

            <div style="
                color:#65747A;
                font-size:0.82rem;
                line-height:1.5;
                margin-top:0.35rem;
            ">
                See how much expected recovery value can be captured
                when the team can only act on part of the queue.
            </div>

        </div>
        """
    )

    capacity = st.slider(
        "Available intervention capacity",
        min_value=0.1,
        max_value=1.0,
        value=0.5,
        step=0.1,
        key="recovery_capacity",
    )

    capacity_percent = int(
        capacity * 100
    )

    result = evaluate_capacity(
        queue,
        capacity
    )

    selected = result[
        "payments_handled"
    ]

    expected_value = result[
        "expected_incremental_value"
    ]

    total_value = queue[
        "expected_incremental_value"
    ].sum()

    capture_rate = (
        expected_value / total_value
        if total_value > 0
        else 0
    )

    left, right = st.columns(
        [1.2, 1],
        gap="large"
    )

    with left:

        render_html(
            f"""
            <div class="tw-card"
                 style="
                     min-height:230px;
                     display:flex;
                     flex-direction:column;
                     justify-content:center;
                 ">

                <div class="tw-card-title">
                    EXPECTED VALUE CAPTURED
                </div>

                <div class="tw-big-number tw-positive"
                     style="
                         font-size:2.5rem;
                         margin-top:0.15rem;
                     ">
                    {format_currency(expected_value)}
                </div>

                <div style="
                    color:#65747A;
                    font-size:0.78rem;
                    margin-top:0.45rem;
                ">
                    From the top {selected}
                    {"payment opportunity"
                     if selected == 1
                     else "payment opportunities"}
                </div>

                <div style="
                    margin-top:1.25rem;
                    height:7px;
                    background:#E6EBE8;
                    border-radius:10px;
                    overflow:hidden;
                ">

                    <div style="
                        width:{capture_rate:.1%};
                        height:100%;
                        background:#4B9B7B;
                        border-radius:10px;
                    "></div>

                </div>

                <div style="
                    display:flex;
                    justify-content:space-between;
                    margin-top:0.5rem;
                    color:#7D898D;
                    font-size:0.68rem;
                ">

                    <span>
                        {capture_rate:.0%} of queue value
                    </span>

                    <span>
                        {selected} / {len(queue)} payments
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
                     min-height:230px;
                     display:flex;
                     flex-direction:column;
                     justify-content:center;
                 ">

                <div class="tw-eyebrow">
                    PRIORITY LOGIC
                </div>

                <div style="
                    color:#17252B;
                    font-size:1.2rem;
                    font-weight:650;
                    line-height:1.2;
                    margin-top:0.2rem;
                ">
                    Strongest opportunities come first.
                </div>

                <div style="
                    color:#65747A;
                    font-size:0.76rem;
                    line-height:1.55;
                    margin-top:0.65rem;
                ">
                    Payment Twin preserves the queue ranking
                    when capacity is constrained, ensuring the
                    highest-value opportunities are handled first.
                </div>

                <div style="
                    margin-top:1.1rem;
                    color:#167C83;
                    font-size:0.72rem;
                    font-weight:750;
                    letter-spacing:0.04em;
                ">
                    {capacity_percent}% CAPACITY
                    · {selected}
                    {"PAYMENT" if selected == 1 else "PAYMENTS"}
                    SELECTED
                </div>

            </div>
            """
        )


# ============================================================
# PAGE
# ============================================================

def render_recovery_queue():

    render_page_header()

    # --------------------------------------------------------
    # Build portfolio once
    # --------------------------------------------------------

    if (
        "recovery_queue_data"
        not in st.session_state
    ):

        with st.spinner(
            "Payment Twin is ranking the recovery portfolio..."
        ):

            policy_decisions = (
                build_demo_portfolio()
            )

            queue = build_recovery_queue(
                policy_decisions
            )

        st.session_state.recovery_queue_data = queue

    else:

        queue = (
            st.session_state.recovery_queue_data
        )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary = summarize_queue(
        queue
    )

    render_summary(
        queue,
        summary
    )

    # --------------------------------------------------------
    # Queue
    # --------------------------------------------------------

    render_queue(
        queue
    )

    # --------------------------------------------------------
    # Capacity
    # --------------------------------------------------------

    render_capacity(
        queue
    )