"""AgriMind AI - dashboard (entry point).

Run from the project root:  streamlit run app/app.py
"""

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
COMPONENTS_DIR = APP_DIR / "Components"

sys.path.insert(0, str(COMPONENTS_DIR))

import streamlit as st  # noqa: E402

from components import (  # noqa: E402
    feature_card,
    footer,
    page_header,
    section_header,
    setup_page,
    steps,
)

setup_page("Dashboard", "🌱")

page_header(
    "Smart Farming Starts with Intelligence.",
    "AgriMind AI turns soil, climate and field data into clear crop and irrigation guidance, "
    "using machine learning models you can use in minutes.",
    icon="leaf",
    large=True,
)

cta1, cta2, _ = st.columns([1, 1, 1.4])
with cta1:
    st.page_link("pages/crop_recommendation.py", label="Recommend a crop", icon=":material/agriculture:")
with cta2:
    st.page_link("pages/irrigation_prediction.py", label="Predict irrigation", icon=":material/water_drop:")

section_header("What you can do", "Two tools, each powered by a trained machine learning model.")
col1, col2 = st.columns(2, gap="large")
with col1:
    feature_card(
        icon="sprout",
        title="Crop Recommendation",
        description="Find the crop best suited to your soil nutrients and growing conditions.",
        points=[
            "Seven inputs: nitrogen, phosphorus, potassium, temperature, humidity, pH and rainfall",
            "The top 3 crops, each with a probability",
            "A chart to compare how close the options are",
        ],
        page="pages/crop_recommendation.py",
        cta="Open Crop Recommendation",
    )
with col2:
    feature_card(
        icon="droplet",
        title="Smart Irrigation Prediction",
        description="Estimate how much irrigation a field needs from its soil, weather and crop details.",
        points=[
            "19 inputs across soil, weather, crop, irrigation and field information",
            "A Low, Medium or High irrigation level",
            "A plain-language explanation of what the level means",
        ],
        page="pages/irrigation_prediction.py",
        cta="Open Irrigation Prediction",
    )

section_header("How it works", "From field data to a decision in three steps.")
steps(
    [
        ("Choose a tool", "Pick crop recommendation or irrigation prediction from the sidebar."),
        ("Enter your field data", "Fill in the soil, weather and field values. Each input shows its unit and valid range."),
        ("Review the result", "Read the prediction, see what it means, and use it alongside local advice."),
    ]
)

footer()
