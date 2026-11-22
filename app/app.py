"""AgriMind AI — application entry point.

Run from the project root:   streamlit run app/app.py

This file only wires things together: page config, theme, navigation and sidebar.
All UI lives in Components/, each tool lives in pages/.
Requires Streamlit >= 1.40 (st.navigation with hidden default nav, keyed containers).
"""
import streamlit as st

from Components import agrimind_ui as shell
from Components.i18n import t

shell.configure_page()   # must be the first Streamlit command
shell.apply_theme()


def dashboard() -> None:
    shell.render_dashboard(PAGES)


PAGES = {
    "dashboard": st.Page(dashboard, title=t("nav_dashboard"), icon=":material/dashboard:", default=True),
    "crop": st.Page("pages/crop_recommendation.py", title=t("nav_crop"),
                    icon=":material/grass:", url_path="crop-recommendation"),
    "irrigation": st.Page("pages/irrigation_prediction.py", title=t("nav_irrigation"),
                          icon=":material/water_drop:", url_path="irrigation-prediction"),
    "yield": st.Page("pages/3_Crop_Yield_Prediction.py", title=t("nav_yield"),
                     icon=":material/trending_up:", url_path="crop-yield-prediction"),
}

navigation = st.navigation(list(PAGES.values()), position="hidden")
shell.render_sidebar(PAGES)
shell.render_topbar()    # brand + language switcher, shown on every page
navigation.run()
