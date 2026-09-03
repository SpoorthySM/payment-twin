import streamlit as st
from textwrap import dedent


def render_html(html, unsafe_allow_html=True):
    """
    Render custom HTML directly.

    st.html() bypasses Streamlit's Markdown parser,
    so HTML is rendered as HTML instead of appearing
    as a code block.
    """

    st.html(
        dedent(html)
    )


def apply_global_styles():

    st.markdown(
        """
<style>

:root {
    --paper: #F5F3EE;
    --surface: #FFFFFF;
    --surface-soft: #EEF3F0;

    --ink: #17252B;
    --ink-soft: #52636A;
    --muted: #7D898D;

    --border: #DDE2DF;

    --teal: #287C83;
    --teal-soft: #E2F0EF;

    --sage: #4E9278;
    --sage-soft: #E7F1EC;

    --coral: #C96C68;
    --coral-soft: #F6E9E7;

    --amber: #C28A4A;
    --amber-soft: #F7EFE2;

    --blue: #709BAE;
}


/* =========================================================
   APPLICATION
   ========================================================= */

.stApp {
    background: var(--paper);
    color: var(--ink);
}

.main .block-container {
    max-width: 1440px;
    padding-top: 2rem;
    padding-bottom: 5rem;
    padding-left: 3.5rem;
    padding-right: 3.5rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* =========================================================
   TYPOGRAPHY
   ========================================================= */

html,
body,
[class*="css"] {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

h1,
h2,
h3 {
    color: var(--ink) !important;
    letter-spacing: -0.04em;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: #ECEBE6;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label {
    color: var(--ink-soft) !important;
    font-size: 0.86rem !important;
    font-weight: 500 !important;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label:hover {
    color: var(--ink) !important;
}


/* =========================================================
   INPUTS
   ========================================================= */

div[data-baseweb="input"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 9px !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 2px rgba(40, 124, 131, 0.10);
}

div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 9px !important;
}

label {
    color: var(--ink-soft) !important;
    font-size: 0.76rem !important;
    font-weight: 600 !important;
}


/* =========================================================
   SIDEBAR NAVIGATION
   ========================================================= */

section[data-testid="stSidebar"] .stButton > button {
    min-height: 38px;
    margin: 0.02rem 0;
    padding: 0.45rem 0.75rem;
    border-radius: 8px;

    background: transparent;
    border: 1px solid transparent;

    color: #52636A;
    font-size: 0.82rem;
    font-weight: 550;

    box-shadow: none;

    transition:
        background 140ms ease,
        color 140ms ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: #E2E5E0;
    color: #17252B;
}

section[data-testid="stSidebar"]
.stButton > button[kind="primary"] {
    background: #DDECE8;
    color: #216C72;
    border: 1px solid #C8DED8;
    font-weight: 650;
}


/* =========================================================
   DATAFRAME
   ========================================================= */

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 11px;
    overflow: hidden;
}


/* =========================================================
   EXPANDERS
   ========================================================= */

div[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 11px;
}


/* =========================================================
   CUSTOM TYPOGRAPHY
   ========================================================= */

.tw-eyebrow {
    color: var(--teal);
    font-size: 0.69rem;
    font-weight: 750;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}

.tw-title {
    color: var(--ink);
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: clamp(2.6rem, 4vw, 3.8rem);
    line-height: 1.08;
    font-weight: 650;
    letter-spacing: -0.025em;
    margin-bottom: 1rem;
}

.tw-subtitle {
    color: var(--ink-soft);
    font-size: 1rem;
    line-height: 1.65;
    max-width: 700px;
}

.tw-line {
    width: 100%;
    height: 1px;
    background: var(--border);
    position: relative;
    margin: 2rem 0;
}

.tw-line::after {
    content: "";
    position: absolute;
    left: 0;
    top: -1px;
    width: 15%;
    min-width: 90px;
    max-width: 190px;
    height: 2px;
    background: var(--teal);
}


/* =========================================================
   CARDS
   ========================================================= */

.tw-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 1.35rem;
    box-shadow: 0 3px 14px rgba(23, 37, 43, 0.035);
}

.tw-card-title {
    color: var(--muted);
    font-size: 0.68rem;
    font-weight: 750;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.tw-big-number {
    color: var(--ink);
    font-size: 2.35rem;
    line-height: 1;
    font-weight: 680;
    letter-spacing: -0.055em;
}

.tw-positive {
    color: var(--sage);
}

.tw-warning {
    color: var(--amber);
}

.tw-negative {
    color: var(--coral);
}

.tw-blue {
    color: var(--blue);
}


/* =========================================================
   RECOMMENDATION
   ========================================================= */

.recommendation {
    background: var(--sage-soft);
    border: 1px solid #CFE2D7;
    border-radius: 14px;
    padding: 1.8rem 2rem;
    position: relative;
    overflow: hidden;
}

.recommendation::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: var(--sage);
}

.recommendation-label {
    color: var(--sage);
    font-size: 0.68rem;
    font-weight: 750;
    letter-spacing: 0.13em;
    text-transform: uppercase;
}

.recommendation-action {
    color: var(--ink);
    font-size: 3rem;
    line-height: 1;
    font-weight: 720;
    letter-spacing: -0.06em;
    margin: 0.45rem 0;
}

.recommendation-probability {
    color: var(--sage);
    font-size: 1.05rem;
    font-weight: 650;
}


/* =========================================================
   STATUS
   ========================================================= */

.status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--sage);
    margin-right: 6px;
    vertical-align: middle;
}


/* =========================================================
   BADGES
   ========================================================= */

.tw-badge {
    display: inline-block;
    padding: 0.35rem 0.65rem;
    border-radius: 999px;
    font-size: 0.67rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}

.tw-badge-teal {
    background: var(--teal-soft);
    color: var(--teal);
}

.tw-badge-green {
    background: var(--sage-soft);
    color: var(--sage);
}

.tw-badge-amber {
    background: var(--amber-soft);
    color: var(--amber);
}

.tw-badge-coral {
    background: var(--coral-soft);
    color: var(--coral);
}


/* =========================================================
   SCROLLBAR
   ========================================================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--paper);
}

::-webkit-scrollbar-thumb {
    background: #C8D0CC;
    border-radius: 10px;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 900px) {

    .main .block-container {
        padding-left: 1.25rem;
        padding-right: 1.25rem;
    }

    .tw-title {
        font-size: 2.7rem;
    }
}

</style>
        """,
        unsafe_allow_html=True
    )