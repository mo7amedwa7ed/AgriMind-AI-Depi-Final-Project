"""Centralized styling for AgriMind AI.

All colors, typography and CSS live here so every page shares one identity.
"""

from __future__ import annotations

import streamlit as st

COLORS = {
    "forest": "#14532D",
    "emerald": "#16A34A",
    "lime": "#84CC16",
    "background": "#F8FAF7",
    "card": "#FFFFFF",
    "text": "#1F2937",
    "muted": "#6B7280",
    "border": "#E3E9E0",
    "teal": "#0F766E",
    "amber": "#D97706",
    "red": "#B91C1C",
}

_FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Fraunces:opsz,wght@9..144,600;9..144,700"
    "&family=Figtree:wght@400;500;600;700&display=swap');"
)

_ROOT_VARS = f"""
:root {{
  --forest: {COLORS['forest']};
  --emerald: {COLORS['emerald']};
  --lime: {COLORS['lime']};
  --bg: {COLORS['background']};
  --card: {COLORS['card']};
  --text: {COLORS['text']};
  --muted: {COLORS['muted']};
  --border: {COLORS['border']};
  --teal: {COLORS['teal']};
  --amber: {COLORS['amber']};
  --red: {COLORS['red']};
  --display: 'Fraunces', Georgia, 'Times New Roman', serif;
  --body: 'Figtree', system-ui, -apple-system, 'Segoe UI', sans-serif;
}}
"""

_CSS = """
/* ---------- Global ---------- */
html, body, .stApp, [data-testid="stAppViewContainer"] {
  font-family: var(--body);
  color: var(--text);
}
.stApp { background: var(--bg); }
[data-testid="stHeader"] { background: transparent; }
#MainMenu, [data-testid="stToolbar"] { visibility: hidden; }
[data-testid="stSidebarNav"] { display: none; }
.block-container { padding: 2rem 2.5rem 3rem; max-width: 1180px; }
h1, h2, h3 { font-family: var(--display); color: var(--forest); letter-spacing: -0.01em; }
p, li { line-height: 1.6; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] { background: var(--forest); border-right: none; }
[data-testid="stSidebar"] [data-testid="stSidebarContent"] { padding-top: 0.5rem; }
.am-brand { display: flex; align-items: center; gap: .7rem; padding: .75rem .25rem 1.25rem; }
.am-brand-mark {
  width: 40px; height: 40px; border-radius: 11px; display: grid; place-items: center;
  background: var(--lime); color: var(--forest);
}
.am-brand-name { font-family: var(--display); font-size: 1.3rem; font-weight: 700; color: #fff; line-height: 1.1; }
.am-brand-tag { font-size: .78rem; color: rgba(255,255,255,.65); }
.am-nav-label { font-size: .8rem; font-weight: 600; color: rgba(255,255,255,.55); margin: .5rem 0 .35rem .25rem; }
.am-side-note {
  margin-top: 1.5rem; padding: .85rem 1rem; border-radius: 12px; font-size: .82rem;
  color: rgba(255,255,255,.78); background: rgba(255,255,255,.07);
}

/* ---------- Page links (navigation + CTAs) ---------- */
[data-testid="stPageLink-NavLink"] {
  border: 1.5px solid var(--emerald); border-radius: 10px; padding: .5rem 1rem;
  background: var(--card); justify-content: center; transition: background .15s ease;
}
[data-testid="stPageLink-NavLink"] p { color: var(--forest) !important; font-weight: 600; margin: 0; }
[data-testid="stPageLink-NavLink"]:hover { background: var(--emerald); }
[data-testid="stPageLink-NavLink"]:hover p { color: #fff !important; }

[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
  border: none; background: transparent; justify-content: flex-start; padding: .6rem .8rem; margin-bottom: .15rem;
}
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] span { color: rgba(255,255,255,.85) !important; font-weight: 500; }
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover { background: rgba(255,255,255,.09); }
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover p { color: #fff !important; }
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] {
  background: rgba(255,255,255,.15); box-shadow: inset 3px 0 0 var(--lime);
}
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] p { color: #fff !important; font-weight: 700; }

/* ---------- Cards (bordered containers) ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
  border: 1px solid var(--border) !important; border-radius: 16px !important; background: var(--card);
  box-shadow: 0 1px 2px rgba(20,83,45,.05), 0 8px 24px rgba(20,83,45,.06);
}
[data-testid="stForm"] { border: none; padding: 0; background: transparent; }

/* ---------- Hero / page header ---------- */
.am-hero {
  position: relative; overflow: hidden; border-radius: 20px; padding: 2rem 2.25rem; margin-bottom: 1.25rem;
  color: #fff; background-color: var(--forest);
  background-image:
    repeating-linear-gradient(100deg, rgba(255,255,255,.045) 0 2px, transparent 2px 26px),
    linear-gradient(135deg, var(--forest) 0%, #166534 100%);
}
.am-hero::after {
  content: ""; position: absolute; right: -60px; bottom: -90px; width: 260px; height: 260px;
  border-radius: 50%; background: radial-gradient(circle, rgba(132,204,22,.35), rgba(132,204,22,0) 70%);
}
.am-hero-row { display: flex; align-items: center; gap: 1rem; position: relative; z-index: 1; }
.am-hero-icon {
  flex: none; width: 52px; height: 52px; border-radius: 14px; display: grid; place-items: center;
  background: var(--lime); color: var(--forest);
}
.am-hero-title { font-family: var(--display); font-size: 2rem; font-weight: 700; margin: 0; color: #fff; line-height: 1.15; }
.am-hero-sub { margin: .35rem 0 0; color: rgba(255,255,255,.82); max-width: 62ch; font-size: 1.02rem; }
.am-hero-lg { padding: 3.25rem 2.5rem; }
.am-hero-lg .am-hero-row { align-items: flex-start; }
.am-hero-lg .am-hero-title { font-size: 3.1rem; max-width: 16ch; line-height: 1.08; }
.am-hero-lg .am-hero-sub { font-size: 1.1rem; margin-top: 1rem; }

/* ---------- Sections ---------- */
.am-section { margin: 1.5rem 0 .75rem; }
.am-section-title { font-family: var(--display); font-size: 1.35rem; font-weight: 700; color: var(--forest); margin: 0; }
.am-section-desc { margin: .15rem 0 0; color: var(--muted); font-size: .95rem; }

/* ---------- Feature cards ---------- */
.am-card-icon {
  width: 48px; height: 48px; border-radius: 13px; display: grid; place-items: center;
  background: #ECFDF3; color: var(--emerald); margin: .5rem 0 .75rem;
}
.am-card-title { font-family: var(--display); font-size: 1.3rem; font-weight: 700; color: var(--forest); margin: 0 0 .35rem; }
.am-card-text { color: var(--text); margin: 0 0 .6rem; }
.am-list { margin: 0 0 1rem; padding-left: 1.1rem; color: var(--muted); font-size: .94rem; }
.am-list li { margin-bottom: .2rem; }
.am-list li::marker { color: var(--emerald); }

/* ---------- Steps ---------- */
.am-steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.am-step { background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 1.25rem 1.35rem; }
.am-step-num {
  width: 32px; height: 32px; border-radius: 50%; display: grid; place-items: center; margin-bottom: .65rem;
  background: var(--forest); color: #fff; font-weight: 700; font-size: .95rem;
}
.am-step-title { font-weight: 700; color: var(--forest); margin: 0 0 .2rem; }
.am-step-text { margin: 0; color: var(--muted); font-size: .94rem; }

/* ---------- Result card ---------- */
.am-result {
  --tone: var(--emerald); --tone-bg: #ECFDF3;
  display: flex; gap: 1.1rem; align-items: flex-start; padding: 1.5rem 1.6rem; border-radius: 18px;
  background: var(--tone-bg); border: 1px solid var(--tone); border-left-width: 7px;
}
.am-result.tone-low { --tone: var(--teal); --tone-bg: #F0FDFA; }
.am-result.tone-medium { --tone: var(--amber); --tone-bg: #FFFBEB; }
.am-result.tone-high { --tone: var(--red); --tone-bg: #FEF2F2; }
.am-result-icon {
  flex: none; width: 48px; height: 48px; border-radius: 13px; display: grid; place-items: center;
  background: var(--tone); color: #fff;
}
.am-result-label { font-size: .88rem; font-weight: 600; color: var(--tone); margin: 0; }
.am-result-value { font-family: var(--display); font-size: 2.5rem; font-weight: 700; line-height: 1.1; color: var(--text); margin: .1rem 0 .4rem; }
.am-result-text { margin: 0; color: var(--text); }
.am-result-foot { margin: .6rem 0 0; font-size: .85rem; color: var(--muted); }

/* ---------- Ranked list ---------- */
.am-rank { display: grid; grid-template-columns: 2rem 1fr 3.8rem; gap: .75rem; align-items: center; padding: .55rem 0; }
.am-rank + .am-rank { border-top: 1px solid var(--border); }
.am-rank-pos { font-weight: 700; color: var(--emerald); }
.am-rank-name { font-weight: 600; margin-bottom: .3rem; }
.am-rank-track { height: 8px; border-radius: 99px; background: #EEF3EB; overflow: hidden; }
.am-rank-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, var(--emerald), var(--lime)); }
.am-rank-pct { text-align: right; font-weight: 700; color: var(--forest); }

/* ---------- Level guide (irrigation) ---------- */
.am-guide { display: grid; grid-template-columns: repeat(3, 1fr); gap: .75rem; margin-top: .75rem; }
.am-guide-item { border-radius: 12px; padding: .8rem 1rem; font-size: .9rem; border: 1px solid var(--border); background: var(--card); }
.am-guide-item b { display: block; margin-bottom: .15rem; }
.am-guide-item.low { border-left: 5px solid var(--teal); }
.am-guide-item.medium { border-left: 5px solid var(--amber); }
.am-guide-item.high { border-left: 5px solid var(--red); }

/* ---------- Inputs ---------- */
[data-testid="stWidgetLabel"] p { font-weight: 600; font-size: .9rem; color: var(--text); }
[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="base-input"] { border-radius: 10px !important; }
[data-baseweb="input"]:focus-within, [data-baseweb="select"] > div:focus-within { border-color: var(--emerald) !important; box-shadow: 0 0 0 2px rgba(22,163,74,.2); }

/* ---------- Primary buttons ---------- */
[data-testid="stFormSubmitButton"] button, .stButton > button[kind="primary"] {
  width: 100%; border: none; border-radius: 12px; padding: .8rem 1.5rem; font-size: 1.05rem; font-weight: 700; color: #fff;
  background: linear-gradient(135deg, var(--forest), var(--emerald));
  box-shadow: 0 6px 16px rgba(22,163,74,.28); transition: transform .15s ease, box-shadow .15s ease;
}
[data-testid="stFormSubmitButton"] button:hover, .stButton > button[kind="primary"]:hover {
  transform: translateY(-1px); box-shadow: 0 10px 22px rgba(22,163,74,.34); color: #fff; border: none;
}
[data-testid="stFormSubmitButton"] button:focus-visible { outline: 3px solid var(--lime); outline-offset: 2px; }

/* ---------- Footer ---------- */
.am-footer { margin-top: 3rem; padding: 1.5rem 0 0; border-top: 1px solid var(--border); color: var(--muted); font-size: .88rem; }
.am-footer b { color: var(--forest); font-family: var(--display); font-size: 1.05rem; }
.am-footer p { margin: .35rem 0 0; max-width: 80ch; }

/* ---------- Responsive ---------- */
@media (max-width: 900px) {
  .am-steps, .am-guide { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .block-container { padding: 1.25rem 1rem 2rem; }
  .am-hero { padding: 1.4rem 1.25rem; }
  .am-hero-title { font-size: 1.55rem; }
  .am-hero-lg { padding: 2rem 1.35rem; }
  .am-hero-lg .am-hero-title { font-size: 2.1rem; }
  .am-result { flex-direction: column; }
  .am-result-value { font-size: 2rem; }
}
"""


def get_css() -> str:
    """Return the full stylesheet as a string."""
    return _FONT_IMPORT + _ROOT_VARS + _CSS


def inject_css() -> None:
    """Inject the global stylesheet into the current Streamlit page."""
    st.markdown(f"<style>{get_css()}</style>", unsafe_allow_html=True)
