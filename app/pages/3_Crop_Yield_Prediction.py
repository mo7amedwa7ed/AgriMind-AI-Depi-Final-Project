"""AgriMind AI - Crop Yield Prediction page.

Pipeline: raw inputs -> 23 encoded features -> saved StandardScaler.transform()
-> saved LinearRegression.predict() -> yield in tons per hectare (t/ha).
Nothing is ever re-fitted.
"""

import math
import sys
from pathlib import Path

PAGE_FILE = Path(__file__).resolve()
APP_DIR = PAGE_FILE.parents[1]
PROJECT_ROOT = PAGE_FILE.parents[2]

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import joblib
import numpy as np
import pandas as pd
import streamlit as st

from Components.components import (  # noqa: E402
    footer,
    page_header,
    probability_chart,
    ranked_list,
    result_card,
    section_header,
    setup_page,
)

# ==========================================================================
# CONFIGURATION
# ==========================================================================

MODEL_PATH = PROJECT_ROOT / "models" / "crop_yield_prediction_model.pkl"
SCALER_PATH = PROJECT_ROOT / "models" / "crop_yield_scaler.pkl"

FEATURE_COLUMNS = [
    "soil_ph",
    "soil_moisture",
    "avg_temperature",
    "total_rainfall",
    "fertilizer_amount",
    "pesticide_usage",
    "sunlight_hours",
    "nitrogen_content",
    "phosphorus_content",
    "potassium_content",
    "irrigation_frequency",
    "month_sin",
    "month_cos",
    "crop_type_Corn",
    "crop_type_Rice",
    "crop_type_Soybean",
    "crop_type_Wheat",
    "region_East",
    "region_North",
    "region_South",
    "region_West",
    "season_Spring",
    "season_Summer",
]

NUMERIC_FEATURES = {
    "soil_ph": (
        "Soil pH", 0.0, 14.0, 0.1,
        "Soil acidity. 7 is neutral."
    ),
    "soil_moisture": (
        "Soil moisture", 0.0, None, 0.1,
        "Soil moisture, in the training data's unit."
    ),
    "avg_temperature": (
        "Average temperature", -50.0, 60.0, 0.1,
        "Average temperature over the growing period."
    ),
    "total_rainfall": (
        "Total rainfall", 0.0, None, 1.0,
        "Total rainfall over the growing period."
    ),
    "fertilizer_amount": (
        "Fertilizer amount", 0.0, None, 0.1,
        "Fertilizer applied."
    ),
    "pesticide_usage": (
        "Pesticide usage", 0.0, None, 0.1,
        "Pesticide applied."
    ),
    "sunlight_hours": (
        "Sunlight hours", 0.0, 24.0, 0.1,
        "Sunlight hours (maximum 24 per day)."
    ),
    "nitrogen_content": (
        "Nitrogen content", 0.0, None, 0.1,
        "Nitrogen content of the soil."
    ),
    "phosphorus_content": (
        "Phosphorus content", 0.0, None, 0.1,
        "Phosphorus content of the soil."
    ),
    "potassium_content": (
        "Potassium content", 0.0, None, 0.1,
        "Potassium content of the soil."
    ),
    "irrigation_frequency": (
        "Irrigation frequency", 0.0, None, 1.0,
        "How often the field is irrigated."
    ),
}

# Default numeric values shown directly inside the input fields.
DEFAULT_NUMERIC_VALUES = {
    "soil_ph": 6.5,
    "soil_moisture": 50.0,
    "avg_temperature": 25.0,
    "total_rainfall": 100.0,
    "fertilizer_amount": 100.0,
    "pesticide_usage": 5.0,
    "sunlight_hours": 8.0,
    "nitrogen_content": 50.0,
    "phosphorus_content": 50.0,
    "potassium_content": 50.0,
    "irrigation_frequency": 3.0,
}

CATEGORICAL_FEATURES = {
    "crop_type": {
        "label": "Crop type",
        "columns": {
            "Corn": "crop_type_Corn",
            "Rice": "crop_type_Rice",
            "Soybean": "crop_type_Soybean",
            "Wheat": "crop_type_Wheat",
        },
    },
    "region": {
        "label": "Region",
        "columns": {
            "East": "region_East",
            "North": "region_North",
            "South": "region_South",
            "West": "region_West",
        },
    },
    "season": {
        "label": "Season",
        "columns": {
            "Spring": "season_Spring",
            "Summer": "season_Summer",
        },
    },
}

DEFAULT_CATEGORIES = {
    "crop_type": "Corn",
    "region": "North",
    "season": "Summer",
}

# These reference categories must be confirmed from the training notebook.
REFERENCE_CATEGORY_NAMES = {
    "crop_type": None,
    "region": None,
    "season": None,
}

MONTHS = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December",
]

DEFAULT_MONTH = "March"

REFERENCE = "__reference__"
Z_WARN = 4.0


# ==========================================================================
# ARTIFACT LOADING
# ==========================================================================

@st.cache_resource(show_spinner=False)
def _load_artifacts(model_path: str, scaler_path: str):
    return joblib.load(model_path), joblib.load(scaler_path)


def _check_artifacts(model, scaler):
    n = len(FEATURE_COLUMNS)

    if not hasattr(model, "predict"):
        return "The model file does not provide a predict() method."

    if not hasattr(scaler, "transform"):
        return "The scaler file does not provide a transform() method."

    for name, obj in (("model", model), ("scaler", scaler)):
        expected = getattr(obj, "n_features_in_", n)

        if expected != n:
            return (
                f"The {name} expects {expected} features, "
                f"but this page builds {n}."
            )

        names = getattr(obj, "feature_names_in_", None)

        if names is not None and list(names) != FEATURE_COLUMNS:
            return (
                f"The {name}'s stored feature names or order differ "
                "from FEATURE_COLUMNS in this page. "
                "Update FEATURE_COLUMNS to match the training notebook."
            )

    return None


def get_artifacts():
    missing = [
        str(p)
        for p in (MODEL_PATH, SCALER_PATH)
        if not p.exists()
    ]

    if missing:
        return (
            None,
            None,
            "Required file(s) not found. Place them at: "
            + "; ".join(missing),
        )

    try:
        model, scaler = _load_artifacts(
            str(MODEL_PATH),
            str(SCALER_PATH),
        )
    except Exception as exc:
        return None, None, f"The model or scaler could not be loaded: {exc}"

    problem = _check_artifacts(model, scaler)

    if problem:
        return None, None, problem

    return model, scaler, None


# ==========================================================================
# PREDICTION LOGIC
# ==========================================================================

def encode_month(month: int) -> tuple[float, float]:
    angle = 2 * np.pi * month / 12
    return float(np.sin(angle)), float(np.cos(angle))


def build_feature_row(values: dict) -> pd.DataFrame:
    row = {col: 0.0 for col in FEATURE_COLUMNS}

    for key in NUMERIC_FEATURES:
        row[key] = float(values[key])

    month_number = MONTHS.index(values["month"]) + 1

    row["month_sin"], row["month_cos"] = encode_month(
        month_number
    )

    for key, cfg in CATEGORICAL_FEATURES.items():
        choice = values[key]

        if choice != REFERENCE:
            row[cfg["columns"][choice]] = 1.0

    return pd.DataFrame(
        [row],
        columns=FEATURE_COLUMNS,
    )


def validate_inputs(values: dict) -> list[str]:
    errors = []

    for key, (label, lo, hi, *_rest) in NUMERIC_FEATURES.items():
        v = values.get(key)

        if v is None:
            errors.append(f"Enter a value for {label}.")

        elif (
            not isinstance(v, (int, float))
            or math.isnan(v)
            or math.isinf(v)
        ):
            errors.append(f"{label} must be a valid number.")

        elif lo is not None and v < lo:
            errors.append(f"{label} must be at least {lo:g}.")

        elif hi is not None and v > hi:
            errors.append(f"{label} must be at most {hi:g}.")

    for key, cfg in CATEGORICAL_FEATURES.items():
        if values.get(key) is None:
            errors.append(f"Select a {cfg['label'].lower()}.")

    if values.get("month") is None:
        errors.append("Select a month.")

    return errors


def unusual_inputs(scaler, row: pd.DataFrame) -> list[str]:
    mean = getattr(scaler, "mean_", None)
    scale = getattr(scaler, "scale_", None)

    if mean is None or scale is None:
        return []

    z = (
        row.iloc[0].to_numpy(dtype=float) - mean
    ) / np.where(scale == 0, 1.0, scale)

    notes = []

    for key, (label, *_rest) in NUMERIC_FEATURES.items():
        score = float(z[FEATURE_COLUMNS.index(key)])

        if abs(score) > Z_WARN:
            notes.append(
                f"{label} ({score:+.1f} standard deviations "
                "from the training mean)"
            )

    return notes


def predict_yield(model, scaler, row: pd.DataFrame) -> float:
    scaled = scaler.transform(row)

    if hasattr(model, "feature_names_in_"):
        scaled = pd.DataFrame(
            scaled,
            columns=FEATURE_COLUMNS,
        )

    return float(np.ravel(model.predict(scaled))[0])


# ==========================================================================
# PAGE UI
# ==========================================================================

setup_page("Crop Yield Prediction", "📈")

page_header(
    "Crop Yield Prediction",
    "Estimate the expected yield, in tons per hectare, "
    "from soil, weather, farm inputs and crop details.",
    icon="chart",
)

model, scaler, load_error = get_artifacts()

if load_error:
    st.error(load_error)
    footer()
    st.stop()


def reference_label(key: str) -> str:
    name = REFERENCE_CATEGORY_NAMES[key]

    return (
        f"{name} (reference category)"
        if name
        else "Other / reference category (unconfirmed)"
    )


def num(col, key: str):
    label, lo, hi, step, help_text = NUMERIC_FEATURES[key]

    return col.number_input(
        label,
        min_value=lo,
        max_value=hi,
        value=DEFAULT_NUMERIC_VALUES[key],
        step=step,
        help=help_text,
        key=f"yield_{key}",
    )


def cat(col, key: str):
    cfg = CATEGORICAL_FEATURES[key]
    options = list(cfg["columns"]) + [REFERENCE]

    return col.selectbox(
        cfg["label"],
        options,
        index=options.index(DEFAULT_CATEGORIES[key]),
        format_func=lambda o, k=key: (
            reference_label(k) if o == REFERENCE else o
        ),
        key=f"yield_{key}",
    )


def reset_form() -> None:
    for k in [
        k for k in st.session_state
        if k.startswith("yield_")
    ]:
        del st.session_state[k]


with st.form("yield_form"):

    vals = {}

    # SOIL
    with st.container(border=True):
        section_header(
            "Soil",
            "Soil condition and nutrient levels.",
        )

        c1, c2, c3 = st.columns(3)

        vals["soil_ph"] = num(c1, "soil_ph")
        vals["soil_moisture"] = num(c2, "soil_moisture")

        c1, c2, c3 = st.columns(3)

        vals["nitrogen_content"] = num(
            c1, "nitrogen_content"
        )
        vals["phosphorus_content"] = num(
            c2, "phosphorus_content"
        )
        vals["potassium_content"] = num(
            c3, "potassium_content"
        )

    # WEATHER
    with st.container(border=True):
        section_header(
            "Weather",
            "Conditions over the growing period.",
        )

        c1, c2, c3 = st.columns(3)

        vals["avg_temperature"] = num(
            c1, "avg_temperature"
        )
        vals["total_rainfall"] = num(
            c2, "total_rainfall"
        )
        vals["sunlight_hours"] = num(
            c3, "sunlight_hours"
        )

    # FARM INPUTS
    with st.container(border=True):
        section_header(
            "Farm inputs",
            "Fertilizer, pesticide and irrigation practice.",
        )

        c1, c2, c3 = st.columns(3)

        vals["fertilizer_amount"] = num(
            c1, "fertilizer_amount"
        )
        vals["pesticide_usage"] = num(
            c2, "pesticide_usage"
        )
        vals["irrigation_frequency"] = num(
            c3, "irrigation_frequency"
        )

    # CROP AND TIMING
    with st.container(border=True):
        section_header(
            "Crop and timing",
            "What is grown, where and when.",
        )

        c1, c2, c3, c4 = st.columns(4)

        vals["crop_type"] = cat(c1, "crop_type")
        vals["region"] = cat(c2, "region")
        vals["season"] = cat(c3, "season")

        vals["month"] = c4.selectbox(
            "Month",
            MONTHS,
            index=MONTHS.index(DEFAULT_MONTH),
            key="yield_month",
        )

    submitted = st.form_submit_button(
        "Predict Crop Yield",
        use_container_width=True,
    )


with st.container(key="yield_reset_container"):
    st.button(
        "Reset inputs",
        on_click=reset_form,
        type="secondary",
        use_container_width=True,
    )


# ==========================================================================
# PREDICTION RESULT
# ==========================================================================

if submitted:

    problems = validate_inputs(vals)

    if problems:
        for p in problems:
            st.error(p)

    else:
        try:
            row = build_feature_row(vals)

            st.session_state["yield_result"] = {
                "value": predict_yield(
                    model,
                    scaler,
                    row,
                ),
                "row": row,
                "unusual": unusual_inputs(
                    scaler,
                    row,
                ),
                "reference_groups": [
                    CATEGORICAL_FEATURES[k]["label"]
                    for k in CATEGORICAL_FEATURES
                    if vals[k] == REFERENCE
                ],
            }

        except Exception as exc:
            st.session_state.pop(
                "yield_result",
                None,
            )
            st.error(
                f"The prediction could not be completed: {exc}"
            )


result = st.session_state.get("yield_result")

if result:

    section_header("Prediction")

    value = result["value"]

    result_card(
        label="Expected crop yield",
        value=f"{value:.2f} t/ha",
        description=(
            "Estimated tons of crop per hectare "
            "for the inputs you entered."
        ),
        icon="chart",
        footnote=(
            "Linear regression model. "
            "Target: yield_tpha (tons per hectare)."
        ),
    )

    if value < 0:
        st.warning(
            "The model returned a negative yield, "
            "which is not physically meaningful. "
            "This usually means some inputs are outside "
            "the range the model was trained on."
        )

    if result["unusual"]:
        st.warning(
            "Some inputs are far outside the training data, "
            "so this estimate may be unreliable: "
            + "; ".join(result["unusual"])
            + "."
        )

    if result["reference_groups"]:
        st.warning(
            "You selected the reference category for: "
            + ", ".join(result["reference_groups"])
            + ". This sets all of that group's encoded "
            "columns to 0. Confirm which category this "
            "represents in your training notebook."
        )

    with st.expander(
        "Show the 23 encoded features sent to the model (before scaling)"
    ):
        st.dataframe(
            result["row"].T.rename(
                columns={0: "value"}
            )
        )

footer()
