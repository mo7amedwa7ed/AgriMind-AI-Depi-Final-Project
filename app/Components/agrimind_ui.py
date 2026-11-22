"""Application shell for AgriMind AI: page config, theme, sidebar, dashboard, page headers."""
from __future__ import annotations

import streamlit as st

from Components import components as ui
from Components import ml, styles
from Components.i18n import LANG_NAMES, SUPPORTED, get_lang, t

PAGE_ICON = "🌱"


# --------------------------------------------------------------------------- #
# Setup
# --------------------------------------------------------------------------- #
def configure_page() -> None:
    """Must be the first Streamlit call of the run (called from app.py)."""
    st.set_page_config(page_title="AgriMind AI", page_icon=PAGE_ICON, layout="wide",
                       initial_sidebar_state="expanded")
    st.session_state.setdefault("lang", "en")


def apply_theme() -> None:
    st.markdown(styles.build_css(get_lang()), unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
_STATUS_LABELS = (("crop", "model_crop"), ("irrigation", "model_irrigation"), ("yield", "model_yield"))


def _status_rows_html() -> str:
    status = ml.model_file_status()
    rows = []
    for key, label_key in _STATUS_LABELS:
        ok = status.get(key, False)
        dot = "ag-dot" if ok else "ag-dot off"
        word = f'<span class="ag-ok">{ui.esc(t("status_ready"))}</span>' if ok else \
            f'<span class="ag-bad">{ui.esc(t("status_missing"))}</span>'
        rows.append(f'<div class="ag-status"><span><span class="{dot}"></span>{ui.esc(t(label_key))}</span>{word}</div>')
    return "".join(rows)


def render_sidebar(pages: dict) -> None:
    with st.sidebar:
        ui.md(
            f'<div class="ag-brand"><div class="ag-logo">{PAGE_ICON}</div><div>'
            f'<div class="ag-brand-name">{ui.esc(t("app_name"))}</div>'
            f'<div class="ag-brand-tag">{ui.esc(t("tagline"))}</div></div></div>'
        )
        ui.md(f'<div class="ag-side-label">{ui.esc(t("nav_section"))}</div>')
        for page in pages.values():
            st.page_link(page)

        ui.md(f'<div class="ag-side-label">{ui.esc(t("language"))}</div>')
        st.radio(
            t("language"), options=list(SUPPORTED), key="lang", horizontal=True,
            format_func=lambda code: LANG_NAMES[code], label_visibility="collapsed",
        )

        ui.md(f'<div class="ag-side-label">{ui.esc(t("system_status"))}</div>')
        ui.md(_status_rows_html())


# --------------------------------------------------------------------------- #
# Shared page pieces
# --------------------------------------------------------------------------- #
def render_page_header(icon: str, title: str, subtitle: str) -> None:
    ui.md(
        f'<div class="ag-page-header"><div class="ag-page-icon">{icon}</div>'
        f"<div><h1>{ui.esc(title)}</h1><p>{ui.esc(subtitle)}</p></div></div>"
    )


def render_footer() -> None:
    ui.md(f'<div class="ag-footer">{ui.esc(t("disclaimer"))}</div>')


# --------------------------------------------------------------------------- #
# Dashboard
# --------------------------------------------------------------------------- #
def render_dashboard(pages: dict) -> None:
    left, right = st.columns([1.7, 1], gap="large")
    with left:
        ui.md(
            f'<div class="ag-hero"><div class="ag-badge">● {ui.esc(t("hero_badge"))}</div>'
            f'<h1 class="ag-hero-title">{ui.esc(t("hero_title"))}</h1>'
            f'<p class="ag-hero-text">{ui.esc(t("hero_text"))}</p></div>'
        )
        with st.container(key="agcta"):
            st.page_link(pages["crop"], label=t("cta_start"), icon=":material/arrow_forward:")
    with right:
        ui.md(f'<div class="ag-panel"><h4>{ui.esc(t("system_status"))}</h4>{_status_rows_html()}</div>')

    # --- feature navigation cards
    ui.section_header(t("features_title"), t("features_sub"))
    cards = (
        ("crop", "🌾", "nav_crop", "card_crop_desc", ("card_crop_tag1", "card_crop_tag2")),
        ("irrigation", "💧", "nav_irrigation", "card_irr_desc", ("card_irr_tag1", "card_irr_tag2")),
        ("yield", "📈", "nav_yield", "card_yield_desc", ("card_yield_tag1", "card_yield_tag2")),
    )
    for col, (page_key, icon, title_key, desc_key, tag_keys), i in zip(st.columns(3, gap="medium"), cards, range(3)):
        with col:
            ui.md(ui.feature_card_html(icon, t(title_key), t(desc_key), [t(k) for k in tag_keys], delay=0.08 * i))
            st.page_link(pages[page_key], label=t("open_tool"), icon=":material/arrow_outward:")

    # --- platform overview
    ui.section_header(t("overview_title"), t("overview_sub"))
    for col, n in zip(st.columns(3, gap="medium"), (1, 2, 3)):
        with col:
            ui.info_card(t(f"ov{n}_t"), t(f"ov{n}_d"))

    # --- how it works
    ui.section_header(t("how_title"), t("how_sub"))
    for col, n in zip(st.columns(3, gap="medium"), (1, 2, 3)):
        with col:
            ui.step_card(n, t(f"how{n}_t"), t(f"how{n}_d"))

    # --- benefits
    ui.section_header(t("ben_title"), t("ben_sub"))
    for col, n in zip(st.columns(4, gap="small"), (1, 2, 3, 4)):
        with col:
            ui.info_card(t(f"ben{n}_t"), t(f"ben{n}_d"), css="ag-benefit")

    render_footer()
