"""Crop Recommendation page — uses models/crop_recommendation_model.pkl (unchanged)."""
import streamlit as st

from Components import agrimind_ui as shell
from Components import components as ui
from Components import ml, styles
from Components.i18n import crop_label, t

NAME = "crop"
# feature -> (min, max, step, starting value).  Bounds are generous widget limits only.
FIELDS = {
    "N": (0.0, 300.0, 1.0, 90.0), "P": (0.0, 300.0, 1.0, 42.0), "K": (0.0, 300.0, 1.0, 43.0),
    "temperature": (-10.0, 60.0, 0.1, 21.0), "humidity": (0.0, 100.0, 0.5, 82.0),
    "ph": (0.0, 14.0, 0.1, 6.5), "rainfall": (0.0, 1000.0, 1.0, 200.0),
}
KEYS = {f: f"crop_{f}" for f in ml.CROP_FEATURES}
DEFAULTS = {KEYS[f]: FIELDS[f][3] for f in ml.CROP_FEATURES}

ui.restore_inputs(DEFAULTS)
shell.render_page_header("🌾", t("crop_title"), t("crop_sub"))


def field(f: str) -> None:
    lo, hi, step, _ = FIELDS[f]
    st.number_input(t(f"crop_{f}"), min_value=lo, max_value=hi, step=step, key=KEYS[f])


left, right = st.columns([1.1, 1], gap="large")
with left:
    with st.container(key="agcard_crop_soil"):
        ui.card_title(t("crop_group_soil"))
        for col, f in zip(st.columns(3), ("N", "P", "K")):
            with col:
                field(f)
    with st.container(key="agcard_crop_climate"):
        ui.card_title(t("crop_group_climate"))
        cols = st.columns(2)
        for i, f in enumerate(("temperature", "humidity", "ph", "rainfall")):
            with cols[i % 2]:
                field(f)

    ui.persist_inputs(KEYS.values())
    values = {f: float(st.session_state[KEYS[f]]) for f in ml.CROP_FEATURES}

    b1, b2 = st.columns([2, 1])
    run = b1.button(t("predict"), type="primary", use_container_width=True, key="crop_predict")
    b2.button(t("reset"), use_container_width=True, key="crop_reset",
              on_click=ui.reset_inputs, args=(DEFAULTS, NAME))
    if run:
        ui.run_and_store(NAME, lambda: ml.predict_crop(values), values)

with right:
    res = ui.load_result(NAME)
    if res is None:
        ui.empty_state("🌾")
    else:
        if res["inputs"] != values:
            ui.callout(t("stale_notice"), "warn")
        payload = res["payload"]
        ranking = payload["ranking"]
        prob = next((p for c, p in ranking if c == payload["label"]), None)
        sub = f'{t("probability")}: {prob * 100:.1f}%' if prob is not None else t("crop_no_proba")
        ui.result_hero(t("crop_kicker"), crop_label(payload["label"]), sub)
        if ranking:
            ui.show_chart(ui.probability_bar_chart(
                [crop_label(c) for c, _ in ranking], [p for _, p in ranking], t("crop_top_chart")))
            st.caption(t("crop_prob_note"))
        with st.expander(t("input_summary")):
            snap = res["inputs"]
            ui.show_chart(ui.value_bar_chart(["N", "P", "K"], [snap["N"], snap["P"], snap["K"]], t("crop_npk_chart")))
            ui.summary_table([(t(f"crop_{f}"), f"{snap[f]:g}") for f in ml.CROP_FEATURES])

shell.render_footer()
