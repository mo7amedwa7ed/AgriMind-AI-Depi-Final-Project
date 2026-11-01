"""Reusable UI components for AgriMind AI."""

from __future__ import annotations

import html
from typing import Sequence

import streamlit as st

from styles import COLORS, inject_css

APP_NAME = "AgriMind AI"

# Inline SVG paths (24x24, stroke based) so no external icon assets are needed.
_ICONS = {
    "leaf": (
        '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>'
        '<path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>'
    ),
    "sprout": (
        '<path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/>'
        '<path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/>'
        '<path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/>'
    ),
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
}


def _html(markup: str) -> str:
    """Collapse indentation so Markdown never treats the HTML as a code block."""
    return "".join(line.strip() for line in markup.splitlines())


def render_html(markup: str) -> None:
    st.markdown(_html(markup), unsafe_allow_html=True)


def icon_svg(name: str, size: int = 24) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{_ICONS.get(name, _ICONS["leaf"])}</svg>'
    )


def _e(value: object) -> str:
    return html.escape(str(value))


# ---------------------------------------------------------------- page setup
def setup_page(title: str, icon: str = "🌱") -> None:
    """Configure the page, inject CSS and draw the sidebar. Call first on every page."""
    st.set_page_config(
        page_title=f"{APP_NAME} - {title}",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()
    render_sidebar()


def render_sidebar() -> None:
    with st.sidebar:
        render_html(
            f"""
            <div class="am-brand">
              <div class="am-brand-mark">{icon_svg("leaf", 22)}</div>
              <div><div class="am-brand-name">{APP_NAME}</div>
              <div class="am-brand-tag">Smart agriculture platform</div></div>
            </div>
            <div class="am-nav-label">Navigate</div>
            """
        )
        # Paths are relative to the entry script (app/app.py).
        st.page_link("app.py", label="Dashboard", icon=":material/dashboard:")
        st.page_link("pages/crop_recommendation.py", label="Crop Recommendation", icon=":material/agriculture:")
        st.page_link("pages/irrigation_prediction.py", label="Irrigation Prediction", icon=":material/water_drop:")
        render_html(
            """
            <div class="am-side-note">Results are model-based decision support.
            Combine them with local agronomic advice and field observation.</div>
            """
        )


# ------------------------------------------------------------------- headers
def page_header(title: str, subtitle: str, icon: str = "leaf", large: bool = False) -> None:
    size = 30 if large else 26
    render_html(
        f"""
        <div class="am-hero{' am-hero-lg' if large else ''}">
          <div class="am-hero-row">
            <div class="am-hero-icon">{icon_svg(icon, size)}</div>
            <div><h1 class="am-hero-title">{_e(title)}</h1>
            <p class="am-hero-sub">{_e(subtitle)}</p></div>
          </div>
        </div>
        """
    )


def section_header(title: str, description: str | None = None) -> None:
    desc = f'<p class="am-section-desc">{_e(description)}</p>' if description else ""
    render_html(f'<div class="am-section"><h2 class="am-section-title">{_e(title)}</h2>{desc}</div>')


# --------------------------------------------------------------------- cards
def feature_card(icon: str, title: str, description: str, points: Sequence[str], page: str, cta: str) -> None:
    """A bordered card with a navigation link to another page."""
    items = "".join(f"<li>{_e(p)}</li>" for p in points)
    with st.container(border=True):
        render_html(
            f"""
            <div class="am-card-icon">{icon_svg(icon, 26)}</div>
            <h3 class="am-card-title">{_e(title)}</h3>
            <p class="am-card-text">{_e(description)}</p>
            <ul class="am-list">{items}</ul>
            """
        )
        st.page_link(page, label=cta)


def steps(items: Sequence[tuple[str, str]]) -> None:
    """A numbered sequence of steps (the content really is ordered)."""
    cards = "".join(
        f'<div class="am-step"><div class="am-step-num">{i}</div>'
        f'<p class="am-step-title">{_e(t)}</p><p class="am-step-text">{_e(d)}</p></div>'
        for i, (t, d) in enumerate(items, start=1)
    )
    render_html(f'<div class="am-steps">{cards}</div>')


def result_card(
    label: str,
    value: str,
    description: str,
    tone: str = "default",
    icon: str = "sprout",
    footnote: str | None = None,
) -> None:
    """Prominent prediction card. tone: default | low | medium | high."""
    foot = f'<p class="am-result-foot">{_e(footnote)}</p>' if footnote else ""
    tone_class = f" tone-{tone}" if tone in {"low", "medium", "high"} else ""
    render_html(
        f"""
        <div class="am-result{tone_class}">
          <div class="am-result-icon">{icon_svg(icon, 26)}</div>
          <div><p class="am-result-label">{_e(label)}</p>
          <div class="am-result-value">{_e(value)}</div>
          <p class="am-result-text">{_e(description)}</p>{foot}</div>
        </div>
        """
    )


def ranked_list(items: Sequence[tuple[str, float]]) -> None:
    """Ranked rows with probability bars. Probabilities are 0-1 floats."""
    rows = "".join(
        f'<div class="am-rank"><div class="am-rank-pos">{i}</div>'
        f'<div><div class="am-rank-name">{_e(name)}</div>'
        f'<div class="am-rank-track"><div class="am-rank-fill" style="width:{max(p * 100, 0.5):.1f}%"></div></div></div>'
        f'<div class="am-rank-pct">{p * 100:.1f}%</div></div>'
        for i, (name, p) in enumerate(items, start=1)
    )
    render_html(f"<div>{rows}</div>")


def level_guide() -> None:
    render_html(
        """
        <div class="am-guide">
          <div class="am-guide-item low"><b>Low</b>Little extra water is needed right now.</div>
          <div class="am-guide-item medium"><b>Medium</b>Moderate watering is advised. Keep monitoring.</div>
          <div class="am-guide-item high"><b>High</b>The field needs significant irrigation soon.</div>
        </div>
        """
    )


def probability_chart(items: Sequence[tuple[str, float]]) -> None:
    """Horizontal bar chart of probabilities (Plotly, with a native fallback)."""
    labels = [n for n, _ in items]
    values = [round(p * 100, 1) for _, p in items]
    try:
        import plotly.graph_objects as go
    except ImportError:
        import pandas as pd

        st.bar_chart(pd.DataFrame({"Probability (%)": values}, index=labels))
        return

    colors = [COLORS["emerald"] if i == 0 else "#B7D88C" for i in range(len(items))]
    fig = go.Figure(go.Bar(x=values, y=labels, orientation="h", marker_color=colors))
    fig.update_traces(texttemplate="%{x}%", textposition="outside", cliponaxis=False)
    fig.update_layout(
        height=100 + 70 * len(items),
        margin=dict(l=0, r=30, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Figtree, sans-serif", color=COLORS["text"], size=14),
        xaxis=dict(range=[0, 100], ticksuffix="%", gridcolor=COLORS["border"], title=None),
        yaxis=dict(autorange="reversed", title=None),
        showlegend=False,
    )
    st.plotly_chart(fig, config={"displayModeBar": False})


# -------------------------------------------------------------------- footer
def footer() -> None:
    render_html(
        f"""
        <div class="am-footer">
          <b>{APP_NAME}</b>
          <p>Machine learning decision support for crop selection and irrigation planning.
          Predictions are estimates, not guarantees, and do not replace advice from a local agronomist.</p>
        </div>
        """
    )
