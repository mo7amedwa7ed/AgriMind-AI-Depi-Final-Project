"""Crop Yield Prediction page — models/crop_yield_prediction_model.pkl + crop_yield_scaler.pkl.

Output is tons per hectare (model) and tons per Egyptian feddan (= ha value x 0.42).
"""
import streamlit as st

from Components import agrimind_ui as shell
from Components import components as ui
from Components import ml
from Components.i18n import t

NAME = "yield"
# feature -> (min, max, step, starting value).  Units follow the training data.
NUM = {
    "soil_ph": (0.0, 14.0, 0.1, 6.5), "soil_moisture": (0.0, 100000.0, 0.5, 30.0),
    "avg_temperature": (-50.0, 80.0, 0.1, 25.0), "total_rainfall": (0.0, 100000.0, 1.0, 600.0),
    "fertilizer_amount": (0.0, 100000.0, 1.0, 150.0), "pesticide_usage": (0.0, 100000.0, 0.5, 5.0),
    "sunlight_hours": (0.0, 24.0, 0.1, 7.0), "nitrogen_content": (0.0, 100000.0, 1.0, 50.0),
    "phosphorus_content": (0.0, 100000.0, 1.0, 30.0), "potassium_content": (0.0, 100000.0, 1.0, 40.0),
    "irrigation_frequency": (0.0, 1000.0, 1.0, 3.0),
}
GROUPS = {
    "yield_group_soil": ("soil_ph", "soil_moisture", "nitrogen_content", "phosphorus_content", "potassium_content"),
    "yield_group_weather": ("avg_temperature", "total_rainfall", "sunlight_hours"),
    "yield_group_farm": ("fertilizer_amount", "pesticide_usage", "irrigation_frequency"),
}
CAT = {  # input -> options (baseline = reference category, all indicator columns 0)
    "crop_type": ml.CROP_TYPE_OPTIONS + [ml.BASELINE],
    "region": ml.REGION_OPTIONS + [ml.BASELINE],
    "season": ml.SEASON_OPTIONS + [ml.BASELINE],
}
KEYS = {n: f"yield_{n}" for n in [*NUM, "month", *CAT]}
DEFAULTS = {KEYS[n]: NUM[n][3] for n in NUM}
DEFAULTS.update({KEYS["month"]: 6, KEYS["crop_type"]: "Wheat", KEYS["region"]: "North", KEYS["season"]: "Spring"})

ui.restore_inputs(DEFAULTS)
shell.render_page_header("📈", t("yield_title"), t("yield_sub"))


def cat_label(v: str) -> str:
    return t("baseline") if v == ml.BASELINE else t(f"val_{v}")


left, right = st.columns([1.15, 1], gap="large")
with left:
    st.caption(t("yield_units_note"))
    for title_key, names in GROUPS.items():
        with st.container(key=f"agcard_{title_key}"):
            ui.card_title(t(title_key))
            cols = st.columns(2)
            for i, n in enumerate(names):
                lo, hi, step, _ = NUM[n]
                with cols[i % 2]:
                    st.number_input(t(f"yield_{n}"), min_value=lo, max_value=hi, step=step, key=KEYS[n])
    with st.container(key="agcard_yield_context"):
        ui.card_title(t("yield_group_context"))
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox(t("yield_month"), options=list(range(1, 13)), key=KEYS["month"],
                         format_func=lambda m: t(f"month_{m}"))
            st.selectbox(t("yield_region"), options=CAT["region"], key=KEYS["region"], format_func=cat_label)
        with c2:
            st.selectbox(t("yield_crop_type"), options=CAT["crop_type"], key=KEYS["crop_type"], format_func=cat_label)
            st.selectbox(t("yield_season"), options=CAT["season"], key=KEYS["season"], format_func=cat_label)
        st.caption(t("yield_baseline_note"))

    ui.persist_inputs(KEYS.values())
    inputs = {n: st.session_state[KEYS[n]] for n in KEYS}

    b1, b2 = st.columns([2, 1])
    run = b1.button(t("predict"), type="primary", use_container_width=True, key="yield_predict")
    b2.button(t("reset"), use_container_width=True, key="yield_reset",
              on_click=ui.reset_inputs, args=(DEFAULTS, NAME))
    if run:
        ui.run_and_store(NAME, lambda: ml.predict_yield(inputs), inputs)

with right:
    res = ui.load_result(NAME)
    if res is None:
        ui.empty_state("📈")
    else:
        if res["inputs"] != inputs:
            ui.callout(t("stale_notice"), "warn")
        p = res["payload"]
        ui.result_hero(t("yield_kicker"), f'{p["tons_per_feddan"]:.2f}', t("yield_per_feddan"),
                       unit=t("yield_unit_feddan"))
        ui.metric_tile(t("yield_ha_label"), f'{p["tons_per_hectare"]:.2f}', t("yield_unit_ha"))
        ui.callout(t("yield_productivity_note"))
        ui.show_chart(ui.value_bar_chart(
            [t("yield_unit_feddan"), t("yield_unit_ha")], [p["tons_per_feddan"], p["tons_per_hectare"]],
            t("yield_chart")))
        with st.expander(t("technical_details")):
            st.caption(t("yield_conversion"))
            st.caption(t("yield_scaler_mode", mode=p["scaler_mode"]))
            snap = res["inputs"]
            rows = [(t(f"yield_{n}"), f"{snap[n]:g}") for n in NUM]
            rows += [(t("yield_month"), t(f"month_{snap['month']}"))]
            rows += [(t(f"yield_{n}"), cat_label(snap[n])) for n in CAT]
            ui.summary_table(rows)

shell.render_footer()
