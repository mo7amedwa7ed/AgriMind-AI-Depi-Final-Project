# 🌱 AgriMind AI

Bilingual (English / Arabic) agricultural AI platform built with Streamlit and scikit-learn.

| Tool | Model | Output |
|---|---|---|
| Crop Recommendation | `models/crop_recommendation_model.pkl` | Recommended crop + class probabilities |
| Irrigation Prediction | `models/irrigation_prediction_model.pkl` (sklearn Pipeline) | Low / Medium / High |
| Crop Yield Prediction | `models/crop_yield_prediction_model.pkl` + `crop_yield_scaler.pkl` | tons / feddan (prominent) and tons / hectare |

Feddan conversion: `yield_ton_per_feddan = yield_ton_per_hectare × 0.42`. These are productivity values, not total farm production.

## Run

```bash
pip install -r requirements.txt     # needs streamlit>=1.40, plotly, scikit-learn, pandas, joblib
streamlit run app/app.py            # run from the project root
```

## Structure

```
app/
  app.py                    entry point: page config, theme, navigation, sidebar
  Components/
    agrimind_ui.py          shell: theme, sidebar, dashboard, page header/footer
    components.py           cards, result blocks, Plotly charts, session-state helpers
    styles.py               palette + full CSS theme + Plotly layout
    i18n.py                 centralized EN/AR translations
    ml.py                   model loading, schema introspection, prediction (no Streamlit)
  pages/                    crop_recommendation.py, irrigation_prediction.py, 3_Crop_Yield_Prediction.py
tests/test_agrimind.py      unit tests (synthetic models only)
Data/ models/ Notebooks/ reports/ src/    untouched
```

## Design notes

* Models are loaded read-only; nothing is retrained, the scaler only ever calls `transform()`.
* **Irrigation schema is never invented.** The input form is generated from the fitted pipeline
  (`feature_names_in_`, ColumnTransformer encoders/scalers). If your pickle does not store column
  names, create `app/irrigation_schema.json`:

```json
{"features": [
  {"name": "Soil_Moisture", "type": "numeric", "default": 30.0},
  {"name": "Soil_Type", "type": "categorical", "options": ["Clay", "Loam", "Sandy"]}
]}
```
  (names must be the exact training columns, in training order.)
* Yield: 23 features in the original order; `month_sin/cos = sin/cos(2π·month/12)`; the unlisted
  reference category of crop type / region / season is offered as "Baseline" (all indicators 0).
* Inputs and results survive page navigation and language switching (own session-state store).

## Tests

```bash
python -m pytest tests -q
```
