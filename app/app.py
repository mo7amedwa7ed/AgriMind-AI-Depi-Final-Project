"""AgriMind AI - dashboard (entry point).

Run from the project root:  streamlit run app/app.py
"""

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import streamlit as st  # noqa: E402

from Components.agrimind_ui import (  # noqa: E402
    feature_card,
    find_page,
    footer,
    page_header,
    section_header,
    setup_page,
    steps,
)

setup_page("Dashboard", "🌱")

# Pages are located by file-name keywords, so links only appear for files that exist.
CROP_REC_PAGE = find_page("recommend")
IRRIGATION_PAGE = find_page("irrigation")
YIELD_PAGE = find_page("yield")

page_header(
    "Smart Farming Starts with Intelligence.",
    "AgriMind AI turns soil, climate and field data into clear crop, irrigation and yield guidance, "
    "using machine learning models.",
    icon="leaf",
    large=True,
)

section_header("What you can do", "Three tools, each powered by a trained machine learning model.")
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    feature_card(
        icon="sprout",
        title="Crop Recommendation",
        description="Find the crop best suited to your soil nutrients and growing conditions.",
        points=["Soil nutrient and climate inputs", "Top crop matches with probabilities"],
        page=CROP_REC_PAGE,
        cta="Open Crop Recommendation",
    )
with col2:
    feature_card(
        icon="droplet",
        title="Irrigation Prediction",
        description="Estimate the irrigation level a field needs from soil, weather, crop and field details.",
        points=["Soil, weather, crop and field inputs", "A Low, Medium or High irrigation level"],
        page=IRRIGATION_PAGE,
        cta="Open Irrigation Prediction",
    )
with col3:
    feature_card(
        icon="chart",
        title="Crop Yield Prediction",
        description="Estimate the expected yield in tons per hectare (t/ha) for a crop, region and season.",
        points=["Soil, weather and farm input values", "Crop, region, season and month"],
        page=YIELD_PAGE,
        cta="Open Crop Yield Prediction",
    )

section_header("How it works", "From field data to a decision in three steps.")
steps(
    [
        ("Choose a tool", "Open any of the three tools from the cards above or the sidebar."),
        ("Enter your field data", "Fill in the soil, weather, crop and field values the tool asks for."),
        ("Review the result", "Read the prediction and use it alongside local advice."),
    ]
)

footer()
