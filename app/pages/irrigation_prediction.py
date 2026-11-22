"""Irrigation Prediction page — uses models/irrigation_prediction_model.pkl (sklearn Pipeline).

The 19-feature input schema is NOT hard-coded: it is read from the fitted pipeline
(or from app/irrigation_schema.json if present), so no input is ever invented.
"""
import streamlit as st

from Components import agrimind_ui as shell
from Components import components as ui
from Components import ml, styles
from Components.i18n import feature_label, irrigation_advice, irrigation_label, t

NAME = "irrigation"
TONES = {"low": styles.LIME, "medium": styles.AMBER, "high": styles.WATER}
ORDER = {"low": 0, "medium": 1, "high": 2}

shell.render_page_header("💧", t("irr_title"), t("irr_sub"))

try:
    specs, source = ml.get_irrigation_schema()
except ml.ModelLoadError as exc:
    ui.callout(t("error_load", detail=exc), "error")
    shell.render_footer()
    st.stop()
except ml.SchemaError as exc:
    ui.callout(f'{t("irr_schema_missing_title")} — {exc}', "error")
    ui.callout(t("irr_schema_missing_body"), "warn")
    shell.render_footer()
    st.stop()

visible = [s for s in specs if s.kind != "unused"]
unused = len(specs) - len(visible)
key_of = {s.name: f"irr_{s.name}" for s in visible}
defaults = {key_of[s.name]: s.default for s in visible}

ui.restore_inputs(defaults)
for s in visible:  # drop stale persisted values that are no longer valid options
    if s.kind == "categorical" and st.session_state[key_of[s.name]] not in s.options:
        st.session_state[key_of[s.name]] = s.default

ui.callout(t("irr_schema_json" if source == "json" else "irr_schema_ok", n=len(specs)))
if len(specs) != 19:
    ui.callout(t("irr_schema_count_warn", n=len(specs)), "warn")
if unused:
    st.caption(t("irr_unused", n=unused))


def widget(s: ml.FeatureSpec) -> None:
    label = feature_label(s.name)
    if s.kind == "categorical":
        st.selectbox(label, options=s.options, key=key_of[s.name], format_func=str)
    else:
        hint = None
        if s.minimum is not None and s.maximum is not None:
            hint = t("irr_training_range", lo=f"{s.minimum:g}", hi=f"{s.maximum:g}")
        step = 1.0 if abs(float(s.default)) >= 100 else 0.1
        st.number_input(label, step=step, key=key_of[s.name], help=hint)


def grid(items: list) -> None:
    cols = st.columns(2)
    for i, s in enumerate(items):
        with cols[i % 2]:
            widget(s)


left, right = st.columns([1.15, 1], gap="large")
with left:
    numeric = [s for s in visible if s.kind == "numeric"]
    categorical = [s for s in visible if s.kind == "categorical"]
    if numeric:
        with st.container(key="agcard_irr_numeric"):
            ui.card_title(t("irr_group_numeric"))
            grid(numeric)
    if categorical:
        with st.container(key="agcard_irr_cat"):
            ui.card_title(t("irr_group_cat"))
            grid(categorical)

    ui.persist_inputs(key_of.values())
    values = {s.name: st.session_state[key_of[s.name]] for s in visible}

    b1, b2 = st.columns([2, 1])
    run = b1.button(t("predict"), type="primary", use_container_width=True, key="irr_predict")
    b2.button(t("reset"), use_container_width=True, key="irr_reset",
              on_click=ui.reset_inputs, args=(defaults, NAME))
    if run:
        ui.run_and_store(NAME, lambda: ml.predict_irrigation(values, specs), values)

with right:
    res = ui.load_result(NAME)
    if res is None:
        ui.empty_state("💧")
    else:
        if res["inputs"] != values:
            ui.callout(t("stale_notice"), "warn")
        payload = res["payload"]
        label = payload["label"]
        tone = TONES.get(str(label).strip().lower(), styles.LIME)
        ui.result_hero(t("irr_kicker"), irrigation_label(label), irrigation_advice(label) or "", accent=tone)
        probs = sorted(payload["probabilities"], key=lambda cp: ORDER.get(str(cp[0]).lower(), 99))
        if probs:
            top = max(p for _, p in probs)
            ui.show_chart(ui.donut_chart(
                [irrigation_label(c) for c, _ in probs], [p for _, p in probs],
                [TONES.get(str(c).lower(), styles.GREEN) for c, _ in probs],
                f"{top * 100:.0f}%", t("irr_chart")))
        with st.expander(t("input_summary")):
            ui.summary_table([(feature_label(s.name), res["inputs"].get(s.name, "")) for s in visible])

shell.render_footer()
