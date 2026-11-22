"""Tests for AgriMind AI.  Run from the project root:  python -m pytest tests -q

They use tiny synthetic scikit-learn models built on the fly (nothing is written to
models/ and no real artifact is modified).  If the real model files exist, read-only
smoke tests also load them and run one prediction.
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from Components import i18n, ml  # noqa: E402


# ------------------------------------------------------------------ fixtures
@pytest.fixture(scope="module")
def yield_artifacts():
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler
    rng = np.random.default_rng(0)
    X = pd.DataFrame(rng.normal(size=(60, 23)), columns=ml.YIELD_FEATURES)
    y = X.sum(axis=1)
    scaler = StandardScaler().fit(X)
    model = LinearRegression().fit(scaler.transform(X), y)
    return model, scaler, scaler.mean_.copy()


@pytest.fixture(scope="module")
def irrigation_pipeline():
    from sklearn.compose import ColumnTransformer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    rng = np.random.default_rng(1)
    df = pd.DataFrame({"moist": rng.uniform(10, 50, 90), "temp": rng.uniform(15, 40, 90),
                       "soil": rng.choice(["Sandy", "Clay", "Loam"], 90)})
    y = rng.choice(["Low", "Medium", "High"], 90)
    pre = ColumnTransformer([("num", StandardScaler(), ["moist", "temp"]),
                             ("cat", OneHotEncoder(), ["soil"])])
    return Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=300))]).fit(df, y)


# ------------------------------------------------------------------ yield
def test_feddan_conversion():
    assert ml.ton_per_feddan(10.0) == pytest.approx(4.2)
    assert ml.FEDDAN_FACTOR == 0.42


def _inputs(**over):
    base = {n: 1.0 for n in ml.YIELD_NUMERIC_INPUTS}
    base.update(month=3, crop_type="Rice", region="East", season="Summer")
    base.update(over)
    return base


def test_yield_row_order_and_encoding():
    row = ml.build_yield_row(_inputs())
    assert list(row) == ml.YIELD_FEATURES and len(row) == 23
    assert row["month_sin"] == pytest.approx(math.sin(2 * math.pi * 3 / 12))
    assert row["month_cos"] == pytest.approx(math.cos(2 * math.pi * 3 / 12))
    assert row["crop_type_Rice"] == 1 and row["crop_type_Corn"] == 0
    assert row["region_East"] == 1 and row["season_Summer"] == 1 and row["season_Spring"] == 0


def test_baseline_category_is_all_zero():
    row = ml.build_yield_row(_inputs(crop_type=ml.BASELINE, region=ml.BASELINE, season=ml.BASELINE))
    assert sum(v for k, v in row.items() if k.startswith(("crop_type_", "region_", "season_"))) == 0


def test_invalid_month_and_category():
    with pytest.raises(ValueError):
        ml.build_yield_row(_inputs(month=13))
    with pytest.raises(ValueError):
        ml.build_yield_row(_inputs(crop_type="Banana"))


def test_yield_prediction_uses_transform_only(yield_artifacts):
    model, scaler, mean_before = yield_artifacts
    out = ml.predict_yield(_inputs(), model=model, scaler=scaler)
    assert out["tons_per_feddan"] == pytest.approx(out["tons_per_hectare"] * 0.42)
    assert np.allclose(scaler.mean_, mean_before)  # never refit
    row = ml.build_yield_row(_inputs())
    expected = model.predict(scaler.transform(pd.DataFrame([row])))[0]
    assert out["tons_per_hectare"] == pytest.approx(expected)


def test_scaler_with_unmappable_width_raises():
    from sklearn.preprocessing import StandardScaler
    bad = StandardScaler().fit(np.random.rand(10, 5))
    with pytest.raises(ml.SchemaError):
        ml.apply_yield_scaler(bad, pd.DataFrame([ml.build_yield_row(_inputs())]))


# ------------------------------------------------------------------ irrigation
def test_schema_is_read_from_pipeline(irrigation_pipeline):
    specs = ml.schema_from_pipeline(irrigation_pipeline)
    assert [s.name for s in specs] == ["moist", "temp", "soil"]
    assert specs[0].kind == "numeric" and specs[2].kind == "categorical"
    assert sorted(specs[2].options) == ["Clay", "Loam", "Sandy"]


def test_irrigation_prediction(irrigation_pipeline):
    specs = ml.schema_from_pipeline(irrigation_pipeline)
    out = ml.predict_irrigation({"moist": 20.0, "temp": 30.0, "soil": "Clay"}, specs, irrigation_pipeline)
    assert out["label"] in {"Low", "Medium", "High"}
    assert sum(p for _, p in out["probabilities"]) == pytest.approx(1.0)


def test_pipeline_without_names_is_not_guessed():
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    pipe = make_pipeline(LogisticRegression()).fit(np.random.rand(20, 4), np.arange(20) % 2)
    with pytest.raises(ml.SchemaError):
        ml.schema_from_pipeline(pipe)


def test_json_schema_override(tmp_path):
    f = tmp_path / "s.json"
    f.write_text('{"features":[{"name":"a","type":"numeric","default":2},'
                 '{"name":"b","type":"categorical","options":["x","y"]}]}')
    specs = ml.schema_from_json(f)
    assert specs[0].default == 2.0 and specs[1].options == ["x", "y"]


# ------------------------------------------------------------------ crop recommendation
def test_crop_prediction_feature_order():
    from sklearn.ensemble import RandomForestClassifier
    rng = np.random.default_rng(2)
    X = pd.DataFrame(rng.uniform(0, 100, (80, 7)), columns=ml.CROP_FEATURES)
    model = RandomForestClassifier(n_estimators=10, random_state=0).fit(X, rng.choice(["rice", "maize", "cotton"], 80))
    vals = {f: 50.0 for f in ml.CROP_FEATURES}
    out = ml.predict_crop(vals, model=model)
    assert out["label"] in {"rice", "maize", "cotton"}
    assert out["ranking"][0][1] >= out["ranking"][-1][1]


# ------------------------------------------------------------------ i18n
def test_translations_complete():
    for key, entry in i18n.TRANSLATIONS.items():
        assert entry.get("en") and entry.get("ar"), key


def test_placeholders_match():
    import re
    for key, entry in i18n.TRANSLATIONS.items():
        assert set(re.findall(r"{(\w+)}", entry["en"])) == set(re.findall(r"{(\w+)}", entry["ar"])), key


def test_labels():
    assert i18n.crop_label("rice", "ar") == "أرز"
    assert i18n.crop_label("rice", "en") == "Rice"
    assert i18n.irrigation_label("low", "ar") == "منخفض"
    assert i18n.t("nav_crop", "ar") != i18n.t("nav_crop", "en")


# ------------------------------------------------------------------ real artifacts (read-only)
@pytest.mark.skipif(not all(ml.model_file_status().values()), reason="model files not present")
def test_real_models_load_and_predict():
    ml.get_crop_model()
    specs, _ = ml.get_irrigation_schema()
    assert specs
    out = ml.predict_yield({**_inputs()})
    assert out["tons_per_feddan"] == pytest.approx(out["tons_per_hectare"] * 0.42)
