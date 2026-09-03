import streamlit as st

from components.styles import render_html


PAGES = [
    "Overview",
    "Analyze Payment",
    "Recovery Queue",
    "Model Intelligence",
    "Methodology",
]


def render_sidebar():

    # --------------------------------------------------------
    # Initialise navigation state
    # --------------------------------------------------------

    if "active_page" not in st.session_state:
        st.session_state.active_page = "Overview"

    with st.sidebar:

        # ----------------------------------------------------
        # Brand
        # ----------------------------------------------------

        render_html(
            """
            <div style="
                padding: 0.35rem 0.15rem 2.1rem 0.15rem;
            ">

                <div style="
                    color:#17252B;
                    font-size:1.18rem;
                    font-weight:700;
                    letter-spacing:-0.035em;
                ">
                    ◈ Payment Twin
                </div>

                <div style="
                    color:#7D898D;
                    font-size:0.62rem;
                    font-weight:650;
                    letter-spacing:0.13em;
                    text-transform:uppercase;
                    margin-top:0.4rem;
                ">
                    Recovery Intelligence
                </div>

            </div>
            """
        )

        # ----------------------------------------------------
        # Workspace label
        # ----------------------------------------------------

        render_html(
            """
            <div style="
                color:#9AA39F;
                font-size:0.62rem;
                font-weight:750;
                letter-spacing:0.14em;
                text-transform:uppercase;
                margin:0 0 0.65rem 0.2rem;
            ">
                Workspace
            </div>
            """
        )

        # ----------------------------------------------------
        # Navigation
        # ----------------------------------------------------

        for page in PAGES:

            selected = (
                st.session_state.active_page == page
            )

            if selected:
                button_type = "primary"
            else:
                button_type = "secondary"

            if st.button(
                page,
                key=f"nav_{page}",
                use_container_width=True,
                type=button_type
            ):
                st.session_state.active_page = page
                st.rerun()

        # ----------------------------------------------------
        # Footer
        # ----------------------------------------------------

        st.markdown(
            """
            <div style="
                position:fixed;
                bottom:1.35rem;
                color:#7D898D;
                font-size:0.67rem;
                line-height:1.7;
            ">
                <span style="color:#4E9278;">●</span>
                System ready<br>
                Payment Twin · v1.0
            </div>
            """,
            unsafe_allow_html=True
        )

    return st.session_state.active_page