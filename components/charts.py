import plotly.graph_objects as go
import streamlit as st


# ============================================================
# Shared Plotly styling
# ============================================================

PAPER = "#FFFFFF"
INK = "#17252B"
MUTED = "#7D898D"
BORDER = "#DDE2DF"
TEAL = "#287C83"
SAGE = "#4E9278"
BLUE = "#709BAE"


def base_layout(
    height=340
):
    return dict(
        height=height,
        margin=dict(
            l=10,
            r=15,
            t=15,
            b=10
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, sans-serif",
            color=MUTED
        ),
        hoverlabel=dict(
            bgcolor=INK,
            font=dict(
                color="white"
            )
        ),
        xaxis=dict(
            showline=False,
            zeroline=False,
            gridcolor=BORDER,
            tickfont=dict(
                size=11
            )
        ),
        yaxis=dict(
            showline=False,
            zeroline=False,
            gridcolor=BORDER,
            tickfont=dict(
                size=11
            )
        ),
        showlegend=False
    )


# ============================================================
# Recovery capacity
# ============================================================

def recovery_capacity_chart():

    capacity = [
        5,
        10,
        20,
        30,
        50
    ]

    recovery = [
        0.559913,
        0.564744,
        0.559543,
        0.557448,
        0.547945
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=capacity,
            y=recovery,
            mode="lines+markers",
            line=dict(
                color=TEAL,
                width=3,
                shape="spline"
            ),
            marker=dict(
                size=8,
                color=SAGE,
                line=dict(
                    color="white",
                    width=2
                )
            ),
            fill="tozeroy",
            fillcolor="rgba(40,124,131,0.07)",
            hovertemplate=(
                "<b>%{x}% capacity</b>"
                "<br>"
                "Recovery: %{y:.1%}"
                "<extra></extra>"
            )
        )
    )

    fig.add_hline(
        y=0.355908,
        line_dash="dot",
        line_color="#AAB5B1",
        line_width=1,
        annotation_text="35.59% overall",
        annotation_font_color=MUTED
    )

    layout = base_layout(350)

    layout.update(
        xaxis=dict(
            title="Intervention capacity",
            ticksuffix="%",
            gridcolor="rgba(0,0,0,0)",
            showline=False,
            zeroline=False
        ),
        yaxis=dict(
            title="Recovery rate",
            tickformat=".0%",
            gridcolor=BORDER,
            showline=False,
            zeroline=False
        )
    )

    fig.update_layout(**layout)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# Ranking lift
# ============================================================

def lift_chart():

    segments = [
        "Top 10%",
        "Top 20%",
        "Top 30%",
        "Top 50%"
    ]

    lift = [
        1.586769,
        1.572156,
        1.566270,
        1.539569
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=segments,
            y=lift,
            marker=dict(
                color=TEAL,
                line=dict(
                    width=0
                )
            ),
            width=0.55,
            hovertemplate=(
                "<b>%{x}</b>"
                "<br>"
                "Lift: %{y:.2f}×"
                "<extra></extra>"
            )
        )
    )

    fig.add_hline(
        y=1,
        line_dash="dot",
        line_color="#AAB5B1",
        line_width=1,
        annotation_text="Random baseline",
        annotation_font_color=MUTED
    )

    layout = base_layout(315)

    layout.update(
        yaxis=dict(
            title="Recovery lift",
            tickformat=".1f×",
            gridcolor=BORDER,
            rangemode="tozero"
        ),
        xaxis=dict(
            gridcolor="rgba(0,0,0,0)"
        )
    )

    fig.update_layout(**layout)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )