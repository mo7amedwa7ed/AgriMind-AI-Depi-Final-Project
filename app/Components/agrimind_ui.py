"""Shared theme and UI helpers used by the dashboard and the Crop Yield page.

This is a NEW file. It does not replace or depend on your existing
Components/components.py or Components/styles.py.
"""

from __future__ import annotations

import html
from pathlib import Path
from typing import Sequence

import streamlit as st

APP_NAME = "AgriMind AI"
APP_DIR = Path(__file__).resolve().parents[1]  # .../app
PAGES_DIR = APP_DIR / "pages"

_FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Fraunces:opsz,wght@9..144,600;9..144,700"
    "&family=Figtree:wght@400;500;600;700&display=swap');"
)

_CSS = """
:root {
  --forest:#14532D; --emerald:#16A34A; --lime:#84CC16; --bg:#F8FAF7; --card:#FFFFFF;
  --text:#1F2937; --muted:#6B7280; --border:#E3E9E0;
  --display:'Fraunces',Georgia,'Times New Roman',serif;
  --body:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif;
}
html, body, .stApp, [data-testid="stAppViewContainer"] { font-family: var(--body); color: var(--text); }
.stApp { background: var(--bg); }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding: 2rem 2.5rem 3rem; max-width: 1180px; }
h1, h2, h3 { font-family: var(--display); color: var(--forest); letter-spacing: -0.01em; }
p, li { line-height: 1.6; }

[data-testid="stSidebar"] {
    background: #14532D;
    border-right: 1px solid #166534;
}

[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    background: #14532D;
}

.am-brand-name {
    color: #FFFFFF;
}

.am-brand-tag {
    color: rgba(255,255,255,.7);
}

.am-nav-label {
    color: rgba(255,255,255,.65);
    font-size: .8rem;
    font-weight: 600;
    margin: .5rem 0 .35rem;
}

[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
    background: transparent;
    border: none;
    justify-content: flex-start;
    padding: .6rem .8rem;
}

[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] span {
    color: white !important;
}

[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
    background: rgba(255,255,255,.12);
}

[data-testid="stPageLink-NavLink"] { border: 1.5px solid var(--emerald); border-radius: 10px; padding: .5rem 1rem; background: var(--card); justify-content: center; transition: background .15s ease; }
[data-testid="stPageLink-NavLink"] p { color: var(--forest) !important; font-weight: 600; margin: 0; }
[data-testid="stPageLink-NavLink"]:hover { background: var(--emerald); }
[data-testid="stPageLink-NavLink"]:hover p { color: #fff !important; }

[data-testid="stVerticalBlockBorderWrapper"] {
  border: 1px solid var(--border) !important; border-radius: 16px !important; background: var(--card);
  box-shadow: 0 1px 2px rgba(20,83,45,.05), 0 8px 24px rgba(20,83,45,.06);
}
[data-testid="stForm"] { border: none; padding: 0; background: transparent; }

.am-hero { position: relative; overflow: hidden; border-radius: 20px; padding: 2rem 2.25rem; margin-bottom: 1.25rem; color: #fff; background-color: var(--forest);
  background-image: repeating-linear-gradient(100deg, rgba(255,255,255,.045) 0 2px, transparent 2px 26px), linear-gradient(135deg, var(--forest) 0%, #166534 100%); }
.am-hero::after { content: ""; position: absolute; right: -60px; bottom: -90px; width: 260px; height: 260px; border-radius: 50%; background: radial-gradient(circle, rgba(132,204,22,.35), rgba(132,204,22,0) 70%); }
.am-hero-row { display: flex; align-items: center; gap: 1rem; position: relative; z-index: 1; }
.am-hero-icon { flex: none; width: 52px; height: 52px; border-radius: 14px; display: grid; place-items: center; background: var(--lime); color: var(--forest); }
.am-hero-title { font-family: var(--display); font-size: 2rem; font-weight: 700; margin: 0; color: #fff; line-height: 1.15; }
.am-hero-sub { margin: .35rem 0 0; color: rgba(255,255,255,.82); max-width: 62ch; font-size: 1.02rem; }
.am-hero-lg { padding: 3.25rem 2.5rem; }
.am-hero-lg .am-hero-row { align-items: flex-start; }
.am-hero-lg .am-hero-title { font-size: 3.1rem; max-width: 16ch; line-height: 1.08; }
.am-hero-lg .am-hero-sub { font-size: 1.1rem; margin-top: 1rem; }

.am-section { margin: 1.5rem 0 .75rem; }
.am-section-title { font-family: var(--display); font-size: 1.35rem; font-weight: 700; color: var(--forest); margin: 0; }
.am-section-desc { margin: .15rem 0 0; color: var(--muted); font-size: .95rem; }

.am-card-icon { width: 48px; height: 48px; border-radius: 13px; display: grid; place-items: center; background: #ECFDF3; color: var(--emerald); margin: .5rem 0 .75rem; }
.am-card-title { font-family: var(--display); font-size: 1.3rem; font-weight: 700; color: var(--forest); margin: 0 0 .35rem; }
.am-card-text { color: var(--text); margin: 0 0 .6rem; }
.am-list { margin: 0 0 1rem; padding-left: 1.1rem; color: var(--muted); font-size: .94rem; }
.am-list li::marker { color: var(--emerald); }
.am-card-missing { color: var(--muted); font-size: .88rem; margin: 0 0 .5rem; }

.am-steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.am-step { background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 1.25rem 1.35rem; }
.am-step-num { width: 32px; height: 32px; border-radius: 50%; display: grid; place-items: center; margin-bottom: .65rem; background: var(--forest); color: #fff; font-weight: 700; font-size: .95rem; }
.am-step-title { font-weight: 700; color: var(--forest); margin: 0 0 .2rem; }
.am-step-text { margin: 0; color: var(--muted); font-size: .94rem; }

.am-result { display: flex; gap: 1.1rem; align-items: flex-start; padding: 1.5rem 1.6rem; border-radius: 18px; background: #ECFDF3; border: 1px solid var(--emerald); border-left-width: 7px; }
.am-result-icon { flex: none; width: 48px; height: 48px; border-radius: 13px; display: grid; place-items: center; background: var(--emerald); color: #fff; }
.am-result-label { font-size: .88rem; font-weight: 600; color: var(--emerald); margin: 0; }
.am-result-value { font-family: var(--display); font-size: 2.6rem; font-weight: 700; line-height: 1.1; color: var(--text); margin: .1rem 0 .4rem; }
.am-result-text { margin: 0; color: var(--text); }
.am-result-foot { margin: .6rem 0 0; font-size: .85rem; color: var(--muted); }

[data-testid="stWidgetLabel"] p { font-weight: 600; font-size: .9rem; color: var(--text); }
[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="base-input"] { border-radius: 10px !important; }
[data-baseweb="input"]:focus-within, [data-baseweb="select"] > div:focus-within { border-color: var(--emerald) !important; box-shadow: 0 0 0 2px rgba(22,163,74,.2); }

[data-testid="stFormSubmitButton"] button {
  width: 100%; border: none; border-radius: 12px; padding: .8rem 1.5rem; font-size: 1.05rem; font-weight: 700; color: #fff;
  background: linear-gradient(135deg, var(--forest), var(--emerald)); box-shadow: 0 6px 16px rgba(22,163,74,.28);
}
[data-testid="stFormSubmitButton"] button:hover { box-shadow: 0 10px 22px rgba(22,163,74,.34); color: #fff; border: none; }
[data-testid="stFormSubmitButton"] button:focus-visible { outline: 3px solid var(--lime); outline-offset: 2px; }

.am-footer { margin-top: 3rem; padding: 1.5rem 0 0; border-top: 1px solid var(--border); color: var(--muted); font-size: .88rem; }
.am-footer b { color: var(--forest); font-family: var(--display); font-size: 1.05rem; }
.am-footer p { margin: .35rem 0 0; max-width: 80ch; }

@media (max-width: 900px) { .am-steps { grid-template-columns: 1fr; } }
@media (max-width: 768px) {
  .block-container { padding: 1.25rem 1rem 2rem; }
  .am-hero { padding: 1.4rem 1.25rem; }
  .am-hero-title { font-size: 1.55rem; }
  .am-hero-lg { padding: 2rem 1.35rem; }
  .am-hero-lg .am-hero-title { font-size: 2.1rem; }
  .am-result { flex-direction: column; }
  .am-result-value { font-size: 2.1rem; }
}
"""

_ICONS = {
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "sprout": (
        '<path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/>'
        '<path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/>'
        '<path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/>'
    ),
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    "chart": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
}


def _html(markup: str) -> str:
    """Collapse indentation so Markdown never treats the HTML as a code block."""
    return "".join(line.strip() for line in markup.splitlines())


def render_html(markup: str) -> None:
    st.markdown(_html(markup), unsafe_allow_html=True)


def _e(value: object) -> str:
    return html.escape(str(value))


def icon_svg(name: str, size: int = 24) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{_ICONS.get(name, _ICONS["leaf"])}</svg>'
    )


def find_page(*keywords: str) -> str | None:
    """Find a page in app/pages whose file name contains every keyword.

    Returns a path relative to app.py (what st.page_link needs), or None.
    This keeps navigation safe even if your page files are named differently.
    """
    if not PAGES_DIR.is_dir():
        return None
    for path in sorted(PAGES_DIR.glob("*.py")):
        name = path.stem.lower()
        if all(k.lower() in name for k in keywords):
            return f"pages/{path.name}"
    return None


def setup_page(title: str, icon: str = "🌱") -> None:
    """Must be the first Streamlit call on a page."""

    st.set_page_config(
        page_title=f"{APP_NAME} - {title}",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(
        f"<style>{_FONT_IMPORT}{_CSS}</style>",
        unsafe_allow_html=True
    )

    with st.sidebar:
        render_html(
            f"""
            <div class="am-brand">
                <div class="am-brand-mark">{icon_svg("leaf", 22)}</div>
                <div>
                    <div class="am-brand-name">{APP_NAME}</div>
                    <div class="am-brand-tag">
                        Smart agriculture platform
                    </div>
                </div>
            </div>
            <div class="am-nav-label">Navigate</div>
            """
        )

        st.page_link("app.py", label="Dashboard",
                     icon=":material/dashboard:")

        st.page_link("pages/crop_recommendation.py",
                     label="Crop Recommendation",
                     icon=":material/agriculture:")

        st.page_link("pages/irrigation_prediction.py",
                     label="Irrigation Prediction",
                     icon=":material/water_drop:")

        st.page_link("pages/3_Crop_Yield_Prediction.py",
                     label="Crop Yield Prediction",
                     icon=":material/monitoring:")


def page_header(title: str, subtitle: str, icon: str = "leaf", large: bool = False) -> None:
    render_html(
        f"""
        <div class="am-hero{' am-hero-lg' if large else ''}"><div class="am-hero-row">
        <div class="am-hero-icon">{icon_svg(icon, 30 if large else 26)}</div>
        <div><h1 class="am-hero-title">{_e(title)}</h1><p class="am-hero-sub">{_e(subtitle)}</p></div>
        </div></div>
        """
    )


def section_header(title: str, description: str | None = None) -> None:
    desc = f'<p class="am-section-desc">{_e(description)}</p>' if description else ""
    render_html(f'<div class="am-section"><h2 class="am-section-title">{_e(title)}</h2>{desc}</div>')


def feature_card(
    icon: str,
    title: str,
    description: str,
    points: Sequence[str],
    page: str | None,
    cta: str
) -> None:
    """Bordered card with aligned navigation buttons."""

    items = "".join(
        f"<li>{_e(p)}</li>" for p in points
    )

    with st.container(border=True):
        render_html(
            f"""
            <div style="min-height: 270px;">
                <div class="am-card-icon">
                    {icon_svg(icon, 26)}
                </div>

                <h3 class="am-card-title">
                    {_e(title)}
                </h3>

                <p class="am-card-text">
                    {_e(description)}
                </p>

                <ul class="am-list">
                    {items}
                </ul>
            </div>
            """
        )

        if page:
            st.page_link(page, label=cta)
        else:
            render_html(
                '<p class="am-card-missing">'
                'This page was not found in app/pages, '
                'so no link is shown.</p>'
            )

def steps(items: Sequence[tuple[str, str]]) -> None:
    cards = "".join(
        f'<div class="am-step"><div class="am-step-num">{i}</div>'
        f'<p class="am-step-title">{_e(t)}</p><p class="am-step-text">{_e(d)}</p></div>'
        for i, (t, d) in enumerate(items, start=1)
    )
    render_html(f'<div class="am-steps">{cards}</div>')


def result_card(label: str, value: str, description: str, icon: str = "chart", footnote: str | None = None) -> None:
    foot = f'<p class="am-result-foot">{_e(footnote)}</p>' if footnote else ""
    render_html(
        f"""
        <div class="am-result"><div class="am-result-icon">{icon_svg(icon, 26)}</div>
        <div><p class="am-result-label">{_e(label)}</p><div class="am-result-value">{_e(value)}</div>
        <p class="am-result-text">{_e(description)}</p>{foot}</div></div>
        """
    )


def footer() -> None:
    render_html(
        f"""
        <div class="am-footer"><b>{APP_NAME}</b>
        <p>Machine learning decision support for farming. Predictions are estimates, not guarantees,
        and do not replace advice from a local agronomist.</p></div>
        """
    )
