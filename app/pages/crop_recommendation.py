"""AgriMind AI - Crop Recommendation page."""

import math
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]  # .../app
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # project root
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from components import (  # noqa: E402
    footer,
    page_header,
    probability_chart,
    ranked_list,
    result_card,
    section_header,
    setup_page,
)

# --------------------------------------------------------------------------
# Model + prediction logic (no UI code below this banner until the page itself)
# --------------------------------------------------------------------------
MODEL_PATH = PROJECT_ROOT / "models" / "crop_recommendation_model.pkl"

# The exact feature order the model was trained with.
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

# (label, min, max, default, step, unit, help)
INPUT_SPECS = {
    "N": ("Nitrogen (N)", 0.0, 140.0, 90.0, 1.0, "kg/ha", "Nitrogen content in the soil. Typical range: 0 to 140."),
    "P": ("Phosphorus (P)", 5.0, 145.0, 42.0, 1.0, "kg/ha", "Phosphorus content in the soil. Typical range: 5 to 145."),
    "K": ("Potassium (K)", 5.0, 205.0, 43.0, 1.0, "kg/ha", "Potassium content in the soil. Typical range: 5 to 205."),
    "temperature": ("Temperature", 8.0, 44.0, 25.0, 0.5, "°C", "Average temperature of the growing area. Typical range: 8 to 44."),
    "humidity": ("Humidity", 14.0, 100.0, 80.0, 1.0, "%", "Average relative humidity. Typical range: 14 to 100."),
    "ph": ("Soil pH", 3.5, 10.0, 6.5, 0.1, "pH", "Acidity of the soil. 7 is neutral; below 7 is acidic. Typical range: 3.5 to 10."),
    "rainfall": ("Rainfall", 20.0, 300.0, 200.0, 1.0, "mm", "Rainfall in the growing area. Typical range: 20 to 300."),
}


@st.cache_resource(show_spinner=False)
def _load_model(path_str: str):
    return joblib.load(path_str)


def get_model():
    """Return (model, error_message). Exactly one of them is None."""
    if not MODEL_PATH.exists():
        return None, (
            "The crop recommendation model was not found. "
            f"Place the trained file at: {MODEL_PATH}"
        )
    try:
        model = _load_model(str(MODEL_PATH))
    except Exception as exc:  # corrupt file, version mismatch, etc.
        return None, f"The crop recommendation model could not be loaded: {exc}"
    if not (hasattr(model, "predict") and hasattr(model, "predict_proba") and hasattr(model, "classes_")):
        return None, "The loaded file is not a classifier with predict(), predict_proba() and classes_."
    expected = getattr(model, "n_features_in_", len(FEATURES))
    if expected != len(FEATURES):
        return None, f"The model expects {expected} features, but this page provides {len(FEATURES)}."
    return model, None


def validate_inputs(values: dict) -> list[str]:
    errors = []
    for key in FEATURES:
        label, lo, hi, *_ = INPUT_SPECS[key]
        v = values.get(key)
        if v is None or not isinstance(v, (int, float)) or math.isnan(v) or math.isinf(v):
            errors.append(f"{label} must be a valid number.")
        elif not lo <= v <= hi:
            errors.append(f"{label} must be between {lo:g} and {hi:g}.")
    return errors


def predict_crop(model, values: dict) -> dict:
    """Run the trained model. Returns the predicted crop and the top 3 probabilities."""
    X = pd.DataFrame([[float(values[f]) for f in FEATURES]], columns=FEATURES)
    predicted = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    classes = list(model.classes_)
    top_idx = np.argsort(proba)[::-1][:3]
    top3 = [(str(classes[i]).title(), float(proba[i])) for i in top_idx]
    confidence = float(proba[classes.index(predicted)])
    return {"crop": str(predicted).title(), "confidence": confidence, "top3": top3}


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------
setup_page("Crop Recommendation", "🌾")

page_header(
    "Crop Recommendation",
    "Enter your soil nutrients and local conditions to see which crops fit best.",
    icon="sprout",
)

model, load_error = get_model()
if load_error:
    st.error(load_error)
    footer()
    st.stop()


def num(col, key: str) -> float:
    label, lo, hi, default, step, unit, help_text = INPUT_SPECS[key]
    return col.number_input(
        f"{label} ({unit})", min_value=lo, max_value=hi, value=default, step=step, help=help_text, key=f"crop_{key}"
    )


with st.form("crop_form"):
    values = {}

    with st.container(border=True):
        section_header("Soil nutrients", "Macronutrients measured in your soil test.")
        c1, c2, c3 = st.columns(3)
        values["N"], values["P"], values["K"] = num(c1, "N"), num(c2, "P"), num(c3, "K")

    with st.container(border=True):
        section_header("Environmental conditions", "Average climate for the growing season.")
        c1, c2, c3 = st.columns(3)
        values["temperature"] = num(c1, "temperature")
        values["humidity"] = num(c2, "humidity")
        values["rainfall"] = num(c3, "rainfall")

    with st.container(border=True):
        section_header("Soil properties", "Acidity affects which nutrients plants can absorb.")
        c1, _, _ = st.columns(3)
        values["ph"] = num(c1, "ph")

    submitted = st.form_submit_button("Recommend Crop", type="primary")

if submitted:
    problems = validate_inputs(values)
    if problems:
        for p in problems:
            st.error(p)
    else:
        try:
            st.session_state["crop_result"] = predict_crop(model, values)
        except Exception as exc:
            st.error(f"The prediction could not be completed: {exc}")

result = st.session_state.get("crop_result")
if result:
    section_header("Recommendation")
    left, right = st.columns([1, 1], gap="large")
    with left:
        result_card(
            label="Best match for your conditions",
            value=result["crop"],
            description="This crop received the highest probability from the model for the values you entered.",
            icon="sprout",
            footnote=f"Model probability: {result['confidence'] * 100:.1f}%",
        )
        section_header("Top 3 crops")
        ranked_list(result["top3"])
    with right:
        section_header("Probability comparison")
        probability_chart(result["top3"])
else:
    st.info("Fill in the values above and select Recommend Crop to see your result.")

footer()
