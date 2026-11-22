"""Reusable UI building blocks for AgriMind AI.

* HTML helpers (``md``, ``esc``) and visual blocks (hero result, tiles, callouts, tables)
* Plotly charts that share the brand theme
* Session-state helpers that keep inputs/results alive across navigation and language
  switches (Streamlit drops the state of widgets that are not rendered on the current page).
"""
from __future__ import annotations

import html as _html
from typing import Any, Iterable

import plotly.graph_objects as go
import streamlit as st

from Components import ml, styles
from Components.i18n import get_lang, t

# --------------------------------------------------------------------------- #
# HTML helpers
# --------------------------------------------------------------------------- #

def esc(value: Any) -> str:
    return _html.escape(str(value))


def md(markup: str) -> None:
    """Render raw HTML.  Lines are stripped & joined so Markdown never treats
    indented HTML as a code block."""
    st.markdown("".join(line.strip() for line in markup.strip().splitlines()), unsafe_allow_html=True)


def section_header(title: str, subtitle: str = "") -> None:
    sub = f"<p>{esc(subtitle)}</p>" if subtitle else ""
    md(f'<div class="ag-section"><h2>{esc(title)}</h2>{sub}<div class="bar"></div></div>')


def card_title(text: str) -> None:
    md(f'<div class="ag-card-title">{esc(text)}</div>')


def feature_card_html(icon: str, title: str, desc: str, tags: Iterable[str], delay: float = 0.0) -> str:
    tag_html = "".join(f'<span class="ag-tag">{esc(x)}</span>' for x in tags)
    return (
        f'<div class="ag-fcard" style="animation-delay:{delay}s">'
        f'<div class="ag-ficon">{icon}</div><div class="ag-ftitle">{esc(title)}</div>'
        f'<p class="ag-fdesc">{esc(desc)}</p><div class="ag-tags">{tag_html}</div></div>'
    )


def info_card(title: str, body: str, css: str = "ag-pillar") -> None:
    md(f'<div class="{css}"><h3>{esc(title)}</h3><p>{esc(body)}</p></div>')


def step_card(num: int, title: str, body: str) -> None:
    md(
        f'<div class="ag-step"><div class="ag-step-num">{num}</div>'
        f"<div><h3>{esc(title)}</h3><p>{esc(body)}</p></div></div>"
    )


def callout(text: str, kind: str = "info") -> None:
    cls = {"warn": " warn", "error": " error"}.get(kind, "")
    md(f'<div class="ag-callout{cls}">{esc(text)}</div>')


def empty_state(icon: str = "🌱") -> None:
    md(
        f'<div class="ag-empty"><div class="ic">{icon}</div>'
        f'<h3>{esc(t("awaiting_title"))}</h3><p>{esc(t("awaiting_text"))}</p></div>'
    )


def result_hero(kicker: str, value: str, sub: str = "", accent: str = styles.LIME, unit: str = "") -> None:
    unit_html = f"<small>{esc(unit)}</small>" if unit else ""
    sub_html = f'<div class="ag-sub">{esc(sub)}</div>' if sub else ""
    md(
        f'<div class="ag-result-hero" style="--accent:{accent}">'
        f'<div class="ag-kicker">{esc(kicker)}</div>'
        f'<div class="ag-value">{esc(value)}{unit_html}</div>{sub_html}</div>'
    )


def metric_tile(label: str, value: str, unit: str = "") -> None:
    unit_html = f"<small>{esc(unit)}</small>" if unit else ""
    md(
        f'<div class="ag-tile"><div class="ag-tile-label">{esc(label)}</div>'
        f'<div class="ag-tile-value">{esc(value)}{unit_html}</div></div>'
    )


def summary_table(rows: list[tuple[str, Any]]) -> None:
    body = "".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in rows)
    md(f'<table class="ag-table">{body}</table>')


# --------------------------------------------------------------------------- #
# Charts
# --------------------------------------------------------------------------- #

def probability_bar_chart(labels: list[str], probs: list[float], title: str) -> go.Figure:
    """Horizontal bar chart of class probabilities (0-100 %)."""
    lang = get_lang()
    values = [p * 100 for p in probs]
    colors = [styles.LIME] + [styles.GREEN] * (len(values) - 1)
    fig = go.Figure(
        go.Bar(
            x=values[::-1], y=labels[::-1], orientation="h",
            marker=dict(color=colors[::-1], line=dict(color=styles.BORDER, width=1)),
            text=[f"{v:.1f}%" for v in values[::-1]], textposition="outside", cliponaxis=False,
            hovertemplate="%{y}: %{x:.2f}%<extra></extra>",
        )
    )
    fig.update_layout(**styles.plotly_layout(lang, height=60 + 52 * len(values), title=title))
    fig.update_xaxes(range=[0, 115], showgrid=True, gridcolor=styles.BORDER, zeroline=False,
                     ticksuffix="%", tickfont=dict(color=styles.MUTED))
    fig.update_yaxes(showgrid=False, tickfont=dict(size=13))
    return fig


def donut_chart(labels: list[str], probs: list[float], colors: list[str], center_text: str, title: str) -> go.Figure:
    lang = get_lang()
    fig = go.Figure(
        go.Pie(
            labels=labels, values=[p * 100 for p in probs], hole=0.68, sort=False,
            marker=dict(colors=colors, line=dict(color=styles.BG, width=3)),
            textinfo="none", hovertemplate="%{label}: %{value:.1f}%<extra></extra>",
        )
    )
    layout = styles.plotly_layout(lang, height=300, title=title)
    layout.update(
        showlegend=True,
        legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center", font=dict(color=styles.TEXT)),
        annotations=[dict(text=f"<b>{center_text}</b>", x=0.5, y=0.5, showarrow=False,
                          font=dict(size=20, color=styles.TEXT))],
    )
    fig.update_layout(**layout)
    return fig


def value_bar_chart(labels: list[str], values: list[float], title: str, highlight: int = 0) -> go.Figure:
    lang = get_lang()
    colors = [styles.LIME if i == highlight else styles.GREEN for i in range(len(values))]
    fig = go.Figure(
        go.Bar(x=labels, y=values, marker=dict(color=colors, line=dict(color=styles.BORDER, width=1)),
               text=[f"{v:.2f}" for v in values], textposition="outside", cliponaxis=False,
               hovertemplate="%{x}: %{y:.3f}<extra></extra>")
    )
    fig.update_layout(**styles.plotly_layout(lang, height=300, title=title), bargap=0.45)
    fig.update_yaxes(showgrid=True, gridcolor=styles.BORDER, zeroline=False, tickfont=dict(color=styles.MUTED),
                     rangemode="tozero")
    fig.update_xaxes(showgrid=False)
    return fig


def show_chart(fig: go.Figure) -> None:
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# --------------------------------------------------------------------------- #
# Session-state persistence (inputs + results)
# --------------------------------------------------------------------------- #
_INPUT_STORE = "_agrimind_inputs"
_RESULT_STORE = "_agrimind_results"


def restore_inputs(defaults: dict[str, Any]) -> None:
    """Call BEFORE creating the widgets.  Re-seeds widget keys from the persistent store
    (Streamlit deletes widget state when a page is left)."""
    store = st.session_state.setdefault(_INPUT_STORE, {})
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = store.get(key, default)


def persist_inputs(keys: Iterable[str]) -> None:
    """Call AFTER the widgets were created."""
    store = st.session_state.setdefault(_INPUT_STORE, {})
    for key in keys:
        if key in st.session_state:
            store[key] = st.session_state[key]


def reset_inputs(defaults: dict[str, Any], result_name: str) -> None:
    """Button callback: restore defaults and drop the stored result."""
    store = st.session_state.setdefault(_INPUT_STORE, {})
    for key, default in defaults.items():
        st.session_state[key] = default
        store[key] = default
    st.session_state.setdefault(_RESULT_STORE, {}).pop(result_name, None)


def save_result(name: str, payload: dict, inputs: dict[str, Any]) -> None:
    st.session_state.setdefault(_RESULT_STORE, {})[name] = {"payload": payload, "inputs": dict(inputs)}


def load_result(name: str) -> dict | None:
    return st.session_state.get(_RESULT_STORE, {}).get(name)


def collect(keys: Iterable[str]) -> dict[str, Any]:
    return {k: st.session_state[k] for k in keys if k in st.session_state}


def run_and_store(name: str, predict_fn, inputs: dict[str, Any]) -> bool:
    """Run a prediction, store its (language-neutral) result, and show a friendly error
    instead of a traceback if anything goes wrong."""
    try:
        payload = predict_fn()
    except ml.ModelLoadError as exc:
        callout(t("error_load", detail=exc), "error")
    except ml.SchemaError as exc:
        callout(t("error_schema", detail=exc), "error")
    except Exception as exc:  # noqa: BLE001 - surface any model error to the user
        callout(t("error_predict", detail=exc), "error")
    else:
        save_result(name, payload, inputs)
        return True
    return False
