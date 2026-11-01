"""AgriMind AI - Irrigation Prediction page."""

import math
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]  # .../app
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # project root
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import joblib  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from components import (  # noqa: E402
    footer,
    level_guide,
    page_header,
    result_card,
    section_header,
    setup_page,
)

# --------------------------------------------------------------------------
# Model + prediction logic
# --------------------------------------------------------------------------
MODEL_PATH = PROJECT_ROOT / "models" / "irrigation_prediction_model.pkl"

# Exactly 19 features, in this order.
FEATURES = [
    "Soil_Type", "Soil_pH", "Soil_Moisture", "Organic_Carbon", "Electrical_Conductivity",
    "Temperature_C", "Humidity", "Rainfall_mm", "Sunlight_Hours", "Wind_Speed_kmh",
    "Crop_Type", "Crop_Growth_Stage", "Season",
    "Irrigation_Type", "Water_Source", "Previous_Irrigation_mm", "Mulching_Used",
    "Field_Area_hectare", "Region",
]

CATEGORIES = {
    "Soil_Type": ["Clay", "Loamy", "Sandy", "Silt"],
    "Crop_Type": ["Cotton", "Maize", "Potato", "Rice", "Sugarcane", "Wheat"],
    "Crop_Growth_Stage": ["Flowering", "Harvest", "Sowing", "Vegetative"],
    "Season": ["Kharif", "Rabi", "Zaid"],
    "Irrigation_Type": ["Canal", "Drip", "Rainfed", "Sprinkler"],
    "Water_Source": ["Groundwater", "Rainwater", "Reservoir", "River"],
    "Mulching_Used": ["No", "Yes"],
    "Region": ["Central", "East", "North", "South", "West"],
}

# feature: (label with unit, min, max, default, step, help)
NUMERIC = {
    "Soil_pH": ("Soil pH", 4.80, 8.20, 6.50, 0.05, "Acidity of the soil. 7 is neutral."),
    "Soil_Moisture": ("Soil moisture (%)", 8.00, 64.99, 30.00, 0.5, "Current water content of the soil."),
    "Organic_Carbon": ("Organic carbon (%)", 0.30, 1.60, 0.80, 0.05, "Organic matter in the soil."),
    "Electrical_Conductivity": ("Electrical conductivity (dS/m)", 0.10, 3.50, 1.50, 0.05, "A measure of soil salinity."),
    "Temperature_C": ("Temperature (°C)", 12.0, 42.0, 28.0, 0.5, "Average air temperature."),
    "Humidity": ("Humidity (%)", 25.00, 94.99, 60.00, 0.5, "Average relative humidity."),
    "Rainfall_mm": ("Rainfall (mm)", 0.38, 2499.69, 800.00, 1.0, "Rainfall for the period."),
    "Sunlight_Hours": ("Sunlight (hours/day)", 4.0, 11.0, 8.0, 0.1, "Average daily sunshine."),
    "Wind_Speed_kmh": ("Wind speed (km/h)", 0.5, 20.0, 8.0, 0.5, "Average wind speed."),
    "Previous_Irrigation_mm": ("Previous irrigation (mm)", 0.02, 119.99, 40.00, 1.0, "Water applied in the last irrigation."),
    "Field_Area_hectare": ("Field area (hectares)", 0.3, 15.0, 3.0, 0.1, "Size of the field."),
}

CATEGORY_LABELS = {
    "Soil_Type": "Soil type", "Crop_Type": "Crop type", "Crop_Growth_Stage": "Growth stage",
    "Season": "Season", "Irrigation_Type": "Irrigation type", "Water_Source": "Water source",
    "Mulching_Used": "Mulching used", "Region": "Region",
}

LEVELS = {
    "low": ("Low irrigation need", "Soil moisture and weather suggest the field needs little extra water right now."),
    "medium": ("Medium irrigation need", "Moderate watering is advised. Keep checking soil moisture and the weather."),
    "high": ("High irrigation need", "The field is likely to need significant irrigation soon to avoid crop stress."),
}


@st.cache_resource(show_spinner=False)
def _load_model(path_str: str):
    return joblib.load(path_str)


def get_model():
    """Return (model, error_message). Exactly one of them is None."""
    if not MODEL_PATH.exists():
        return None, (
            "The irrigation prediction model was not found. "
            f"Place the trained file at: {MODEL_PATH}"
        )
    try:
        model = _load_model(str(MODEL_PATH))
    except Exception as exc:
        return None, f"The irrigation prediction model could not be loaded: {exc}"
    if not hasattr(model, "predict"):
        return None, "The loaded file does not provide a predict() method."
    names = getattr(model, "feature_names_in_", None)
    if names is not None and set(names) != set(FEATURES):
        missing = sorted(set(names) - set(FEATURES))
        extra = sorted(set(FEATURES) - set(names))
        return None, f"Model features differ from this page. Missing: {missing or 'none'}. Unexpected: {extra or 'none'}."
    return model, None


def validate_inputs(values: dict) -> list[str]:
    errors = []
    for key, (label, lo, hi, *_rest) in NUMERIC.items():
        v = values.get(key)
        if not isinstance(v, (int, float)) or math.isnan(v) or math.isinf(v):
            errors.append(f"{label} must be a valid number.")
        elif not lo <= v <= hi:
            errors.append(f"{label} must be between {lo:g} and {hi:g}.")
    for key, options in CATEGORIES.items():
        if values.get(key) not in options:
            errors.append(f"{CATEGORY_LABELS[key]} must be one of: {', '.join(options)}.")
    return errors


def predict_irrigation(model, values: dict) -> str:
    """Raw values go straight to the Pipeline, which handles all encoding."""
    X = pd.DataFrame([{f: values[f] for f in FEATURES}], columns=FEATURES)
    names = getattr(model, "feature_names_in_", None)
    if names is not None:
        X = X[list(names)]
    return str(model.predict(X)[0])


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------
setup_page("Irrigation Prediction", "💧")

page_header(
    "Irrigation Prediction",
    "Describe your soil, weather, crop and field to estimate the irrigation level it needs.",
    icon="droplet",
)

model, load_error = get_model()
if load_error:
    st.error(load_error)
    footer()
    st.stop()


def num(col, key: str) -> float:
    label, lo, hi, default, step, help_text = NUMERIC[key]
    return col.number_input(
        label, min_value=lo, max_value=hi, value=default, step=step, format="%.2f", help=help_text, key=f"irr_{key}"
    )


def cat(col, key: str, help_text: str | None = None) -> str:
    return col.selectbox(CATEGORY_LABELS[key], CATEGORIES[key], help=help_text, key=f"irr_{key}")


with st.form("irrigation_form"):
    v = {}

    with st.container(border=True):
        section_header("Soil information", "Soil type and the latest soil test readings.")
        c1, c2, c3 = st.columns(3)
        v["Soil_Type"] = cat(c1, "Soil_Type")
        v["Soil_pH"] = num(c2, "Soil_pH")
        v["Soil_Moisture"] = num(c3, "Soil_Moisture")
        c1, c2, _ = st.columns(3)
        v["Organic_Carbon"] = num(c1, "Organic_Carbon")
        v["Electrical_Conductivity"] = num(c2, "Electrical_Conductivity")

    with st.container(border=True):
        section_header("Weather conditions", "Average conditions for the period you are planning.")
        c1, c2, c3 = st.columns(3)
        v["Temperature_C"] = num(c1, "Temperature_C")
        v["Humidity"] = num(c2, "Humidity")
        v["Rainfall_mm"] = num(c3, "Rainfall_mm")
        c1, c2, _ = st.columns(3)
        v["Sunlight_Hours"] = num(c1, "Sunlight_Hours")
        v["Wind_Speed_kmh"] = num(c2, "Wind_Speed_kmh")

    with st.container(border=True):
        section_header("Crop information", "What is growing and where it is in its cycle.")
        c1, c2, c3 = st.columns(3)
        v["Crop_Type"] = cat(c1, "Crop_Type")
        v["Crop_Growth_Stage"] = cat(c2, "Crop_Growth_Stage")
        v["Season"] = cat(c3, "Season", "Kharif: monsoon, Rabi: winter, Zaid: summer.")

    with st.container(border=True):
        section_header("Irrigation information", "How the field is watered today.")
        c1, c2 = st.columns(2)
        v["Irrigation_Type"] = cat(c1, "Irrigation_Type")
        v["Water_Source"] = cat(c2, "Water_Source")
        c1, c2 = st.columns(2)
        v["Previous_Irrigation_mm"] = num(c1, "Previous_Irrigation_mm")
        v["Mulching_Used"] = c2.radio(
            CATEGORY_LABELS["Mulching_Used"], CATEGORIES["Mulching_Used"], horizontal=True,
            help="Mulch covers the soil surface to reduce evaporation.", key="irr_Mulching_Used",
        )

    with st.container(border=True):
        section_header("Field information", "Size and location of the field.")
        c1, c2, _ = st.columns(3)
        v["Field_Area_hectare"] = num(c1, "Field_Area_hectare")
        v["Region"] = cat(c2, "Region")

    submitted = st.form_submit_button("Predict Irrigation Level", type="primary")

if submitted:
    problems = validate_inputs(v)
    if problems:
        for p in problems:
            st.error(p)
    else:
        try:
            st.session_state["irrigation_result"] = predict_irrigation(model, v)
        except Exception as exc:
            st.error(f"The prediction could not be completed: {exc}")

result = st.session_state.get("irrigation_result")
if result:
    section_header("Prediction")
    key = result.strip().lower()
    if key in LEVELS:
        title, text = LEVELS[key]
        result_card(
            label="Predicted irrigation level", value=result.strip().title(), description=text,
            tone=key, icon="droplet", footnote=title,
        )
    else:
        result_card(
            label="Predicted irrigation level", value=result, description="", tone="default", icon="droplet",
        )
    section_header("What the levels mean")
    level_guide()
else:
    st.info("Fill in the details above and select Predict Irrigation Level to see your result.")
    level_guide()

footer()
