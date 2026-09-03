import streamlit as st

from components.styles import (
    apply_global_styles,
    render_html
)

from components.navigation import render_sidebar
from views.overview import render_overview
from views.analyze import render_analyze
from views.recovery_queue import render_recovery_queue
from views.model_intelligence import render_model_intelligence
from views.methodology import render_methodology


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Payment Twin",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GLOBAL STYLE
# ============================================================

apply_global_styles()


# ============================================================
# SIDEBAR
# ============================================================

page = render_sidebar()

# ============================================================
# PAGE ROUTING
# ============================================================

if page == "Overview":

    render_overview()


elif page == "Analyze Payment":

    render_analyze()


elif page == "Recovery Queue":

    render_recovery_queue()

elif page == "Model Intelligence":

    render_model_intelligence()


elif page == "Methodology":

    render_methodology()

    render_html(
        """
        <div class="tw-eyebrow">
            METHODOLOGY
        </div>

        <div class="tw-title">
            How Payment Twin works.
        </div>

        <div class="tw-subtitle">
            The modelling, decision, prioritization,
            explainability, and evaluation framework behind
            the system.
        </div>
        """
    )

