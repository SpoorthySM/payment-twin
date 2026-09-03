import streamlit as st

from components.styles import render_html


def metric_block(
    label,
    value,
    description="",
    accent=""
):

    accent_class = ""

    if accent:
        accent_class = f"tw-{accent}"

    render_html(
        f"""
        <div class="tw-card" style="height:100%;">

            <div class="tw-card-title">
                {label}
            </div>

            <div class="tw-big-number {accent_class}">
                {value}
            </div>

            <div style="
                color:#7D898D;
                font-size:0.74rem;
                margin-top:0.65rem;
                line-height:1.45;
            ">
                {description}
            </div>

        </div>
        """
    )


def section_header(
    eyebrow,
    title,
    description=""
):

    render_html(
        f"""
        <div style="margin-bottom:1.4rem;">

            <div class="tw-eyebrow">
                {eyebrow}
            </div>

            <div style="
                color:#17252B;
                font-size:1.7rem;
                font-weight:680;
                letter-spacing:-0.045em;
                line-height:1.15;
            ">
                {title}
            </div>

            <div style="
                color:#65747A;
                font-size:0.84rem;
                margin-top:0.45rem;
                max-width:680px;
                line-height:1.55;
            ">
                {description}
            </div>

        </div>
        """
    )