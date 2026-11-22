"""Model loading, schema handling and prediction logic for AgriMind AI.

Design rules (from the upgrade brief)
-------------------------------------
* The trained artifacts in ``models/`` are only ever READ (never written, never refit).
* Feature order for crop yield is the exact 23-feature order of the original app.
* The crop-yield scaler is used with ``transform()`` only.
* The irrigation input schema is NOT invented: it is read from the trained
  Scikit-learn pipeline itself (or from an explicit ``app/irrigation_schema.json``).

This module deliberately does not import Streamlit so it can be tested stand-alone.
"""
from __future__ import annotations

import json
import math
import os
import pickle
import warnings
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Paths  (app/Components/ml.py -> app/ -> project root)
# --------------------------------------------------------------------------- #
APP_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = APP_DIR.parent


def models_dir() -> Path:
    """models/ folder (can be overridden with AGRIMIND_MODELS_DIR, used by tests)."""
    override = os.environ.get("AGRIMIND_MODELS_DIR")
    return Path(override) if override else PROJECT_ROOT / "models"


CROP_MODEL_FILE = "crop_recommendation_model.pkl"
IRRIGATION_MODEL_FILE = "irrigation_prediction_model.pkl"
YIELD_MODEL_FILE = "crop_yield_prediction_model.pkl"
YIELD_SCALER_FILE = "crop_yield_scaler.pkl"
IRRIGATION_SCHEMA_FILE = APP_DIR / "irrigation_schema.json"


class ModelLoadError(RuntimeError):
    """A model/scaler file is missing or unreadable."""


class SchemaError(RuntimeError):
    """The input schema cannot be verified or does not match the model."""


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
@lru_cache(maxsize=None)
def _load(path_str: str):
    path = Path(path_str)
    if not path.exists():
        raise ModelLoadError(f"{path.name} not found in {path.parent}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # sklearn version-mismatch notices
        try:
            import joblib

            return joblib.load(path)
        except Exception as first_error:
            try:
                with open(path, "rb") as fh:
                    return pickle.load(fh)
            except Exception as second_error:
                raise ModelLoadError(f"{path.name}: {second_error or first_error}") from second_error


def clear_cache() -> None:
    _load.cache_clear()


def get_crop_model():
    return _load(str(models_dir() / CROP_MODEL_FILE))


def get_irrigation_model():
    return _load(str(models_dir() / IRRIGATION_MODEL_FILE))


def get_yield_model():
    return _load(str(models_dir() / YIELD_MODEL_FILE))


def get_yield_scaler():
    return _load(str(models_dir() / YIELD_SCALER_FILE))


def model_file_status() -> dict[str, bool]:
    """Whether each model group's files exist on disk (no loading, no side effects)."""
    d = models_dir()
    return {
        "crop": (d / CROP_MODEL_FILE).exists(),
        "irrigation": (d / IRRIGATION_MODEL_FILE).exists(),
        "yield": (d / YIELD_MODEL_FILE).exists() and (d / YIELD_SCALER_FILE).exists(),
    }


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _py(value: Any):
    """numpy scalar -> plain Python scalar."""
    if isinstance(value, np.generic):
        return value.item()
    return value


def _model_input(model, row: dict[str, float], order: list[str]):
    """Build the model input in the ORIGINAL feature order.

    * If the estimator remembers its column names and they match ``order`` as a set,
      a DataFrame in the estimator's own order is returned.
    * Otherwise a positional float array in ``order`` is returned (the original order).
    """
    names = getattr(model, "feature_names_in_", None)
    if names is not None:
        names = [str(n) for n in names]
        if set(names) == set(order):
            return pd.DataFrame([[row[n] for n in names]], columns=names)
        if len(names) != len(order):
            raise SchemaError(
                f"model expects {len(names)} features, the app provides {len(order)}"
            )
    return np.array([[float(row[c]) for c in order]], dtype=float)


def _probabilities(model, X) -> tuple[list, list[float]] | None:
    if not hasattr(model, "predict_proba"):
        return None
    try:
        proba = np.asarray(model.predict_proba(X))[0]
        classes = [_py(c) for c in getattr(model, "classes_", range(len(proba)))]
        return classes, [float(p) for p in proba]
    except Exception:
        return None


# --------------------------------------------------------------------------- #
# A. Crop recommendation
# --------------------------------------------------------------------------- #
CROP_FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]


def predict_crop(values: dict[str, float], model=None, top_k: int = 5) -> dict:
    model = model if model is not None else get_crop_model()
    X = _model_input(model, values, CROP_FEATURES)
    label = _py(np.ravel(model.predict(X))[0])
    result: dict[str, Any] = {"label": label, "ranking": []}
    proba = _probabilities(model, X)
    if proba:
        classes, probs = proba
        order = np.argsort(probs)[::-1][:top_k]
        result["ranking"] = [(classes[i], probs[i]) for i in order]
    return result


# --------------------------------------------------------------------------- #
# B. Irrigation prediction  (schema read from the trained pipeline)
# --------------------------------------------------------------------------- #
@dataclass
class FeatureSpec:
    name: str
    kind: str = "numeric"  # numeric | categorical | unused
    default: Any = 0.0
    options: list = field(default_factory=list)
    minimum: float | None = None
    maximum: float | None = None


def _inner_steps(obj) -> list:
    steps = getattr(obj, "steps", None)
    if steps:
        out = []
        for _, step in steps:
            out.extend(_inner_steps(step))
        return out
    return [obj]


def _find_column_transformer(obj):
    from sklearn.compose import ColumnTransformer

    if isinstance(obj, ColumnTransformer):
        return obj
    for step in _inner_steps_shallow(obj):
        found = _find_column_transformer(step)
        if found is not None:
            return found
    return None


def _inner_steps_shallow(obj) -> list:
    steps = getattr(obj, "steps", None)
    return [s for _, s in steps] if steps else []


def _column_names_for(ct, name: str, cols, names: list[str]) -> list[str]:
    idx_map = getattr(ct, "_transformer_to_input_indices", None)
    if isinstance(idx_map, dict) and name in idx_map and names:
        return [names[i] for i in idx_map[name]]
    if isinstance(cols, (str, int)):
        cols = [cols]
    if isinstance(cols, slice):
        return names[cols]
    out = []
    for c in list(cols):
        if isinstance(c, (int, np.integer)) and not isinstance(c, bool) and names:
            out.append(names[int(c)])
        else:
            out.append(str(c))
    return out


def _clean_num(x) -> float:
    x = float(x)
    return 0.0 if (math.isnan(x) or math.isinf(x)) else round(x, 6)


def schema_from_pipeline(model) -> list[FeatureSpec]:
    """Derive input specs from a FITTED sklearn pipeline.  Never invents columns."""
    names = getattr(model, "feature_names_in_", None)
    if names is None:
        raise SchemaError("the saved pipeline does not store its input column names")
    names = [str(n) for n in names]

    specs: dict[str, FeatureSpec] = {}
    ct = _find_column_transformer(model)
    if ct is not None and hasattr(ct, "transformers_"):
        for name, trans, cols in ct.transformers_:
            if isinstance(trans, str) and trans == "drop":
                for c in _column_names_for(ct, name, cols, names):
                    specs[c] = FeatureSpec(c, "unused", 0.0)
                continue
            col_names = _column_names_for(ct, name, cols, names)
            inner = [] if isinstance(trans, str) else _inner_steps(trans)
            cat_enc = next((s for s in inner if hasattr(s, "categories_")), None)
            scaler = next((s for s in inner if getattr(s, "mean_", None) is not None), None)
            minmax = next((s for s in inner if hasattr(s, "data_min_") and hasattr(s, "data_max_")), None)
            imputer = next((s for s in inner if hasattr(s, "statistics_")), None)
            for i, col in enumerate(col_names):
                if cat_enc is not None:
                    cats = [_py(c) for c in cat_enc.categories_[i]]
                    specs[col] = FeatureSpec(col, "categorical", cats[0] if cats else "", cats)
                    continue
                spec = FeatureSpec(col, "numeric", 0.0)
                try:
                    if scaler is not None:
                        spec.default = _clean_num(scaler.mean_[i])
                    elif minmax is not None:
                        spec.default = _clean_num((minmax.data_min_[i] + minmax.data_max_[i]) / 2)
                    elif imputer is not None:
                        spec.default = _clean_num(imputer.statistics_[i])
                    if minmax is not None:
                        spec.minimum = _clean_num(minmax.data_min_[i])
                        spec.maximum = _clean_num(minmax.data_max_[i])
                except Exception:
                    pass
                specs[col] = spec
    # Pipeline without a ColumnTransformer (or columns it did not mention): numeric
    for n in names:
        specs.setdefault(n, FeatureSpec(n, "numeric", 0.0))
    return [specs[n] for n in names]


def schema_from_json(path: Path) -> list[FeatureSpec]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    specs = []
    for item in data["features"]:
        kind = item.get("type", "numeric")
        if kind == "categorical":
            options = list(item["options"])
            specs.append(FeatureSpec(item["name"], "categorical", item.get("default", options[0]), options))
        else:
            specs.append(
                FeatureSpec(item["name"], "numeric", float(item.get("default", 0.0)),
                            minimum=item.get("min"), maximum=item.get("max"))
            )
    return specs


def get_irrigation_schema(model=None, schema_path: Path | None = None) -> tuple[list[FeatureSpec], str]:
    """Return (specs, source) where source is "json" or "pipeline"."""
    path = schema_path if schema_path is not None else IRRIGATION_SCHEMA_FILE
    if Path(path).exists():
        try:
            return schema_from_json(path), "json"
        except Exception as exc:
            raise SchemaError(f"irrigation_schema.json is invalid: {exc}") from exc
    model = model if model is not None else get_irrigation_model()
    return schema_from_pipeline(model), "pipeline"


def irrigation_defaults(specs: list[FeatureSpec]) -> dict[str, Any]:
    return {s.name: s.default for s in specs}


def predict_irrigation(values: dict[str, Any], specs: list[FeatureSpec] | None = None, model=None) -> dict:
    model = model if model is not None else get_irrigation_model()
    if specs is None:
        specs, _ = get_irrigation_schema(model)
    row = {}
    for s in specs:
        if s.kind == "unused":
            row[s.name] = 0.0
        elif s.kind == "numeric":
            row[s.name] = float(values[s.name])
        else:
            row[s.name] = values[s.name]
    frame = pd.DataFrame([row], columns=[s.name for s in specs])  # pipeline does its own preprocessing
    label = _py(np.ravel(model.predict(frame))[0])
    result: dict[str, Any] = {"label": label, "probabilities": []}
    proba = _probabilities(model, frame)
    if proba:
        result["probabilities"] = list(zip(*proba))
    return result


# --------------------------------------------------------------------------- #
# C. Crop yield prediction
# --------------------------------------------------------------------------- #
YIELD_FEATURES = [
    "soil_ph", "soil_moisture", "avg_temperature", "total_rainfall", "fertilizer_amount",
    "pesticide_usage", "sunlight_hours", "nitrogen_content", "phosphorus_content",
    "potassium_content", "irrigation_frequency", "month_sin", "month_cos",
    "crop_type_Corn", "crop_type_Rice", "crop_type_Soybean", "crop_type_Wheat",
    "region_East", "region_North", "region_South", "region_West",
    "season_Spring", "season_Summer",
]
YIELD_NUMERIC_INPUTS = YIELD_FEATURES[:11]
CROP_TYPE_OPTIONS = ["Corn", "Rice", "Soybean", "Wheat"]
REGION_OPTIONS = ["East", "North", "South", "West"]
SEASON_OPTIONS = ["Spring", "Summer"]
BASELINE = "__baseline__"  # reference category: every indicator column stays 0

FEDDAN_FACTOR = 0.42  # yield_ton_per_feddan = yield_ton_per_hectare * 0.42


def ton_per_feddan(ton_per_hectare: float) -> float:
    return ton_per_hectare * FEDDAN_FACTOR


def build_yield_row(inputs: dict[str, Any]) -> dict[str, float]:
    """Raw (unscaled) 23-feature row in the original order."""
    month = int(inputs["month"])
    if not 1 <= month <= 12:
        raise ValueError("month must be between 1 and 12")
    row: dict[str, float] = {k: float(inputs[k]) for k in YIELD_NUMERIC_INPUTS}
    angle = 2 * math.pi * month / 12
    row["month_sin"] = math.sin(angle)
    row["month_cos"] = math.cos(angle)
    for prefix, options, chosen in (
        ("crop_type", CROP_TYPE_OPTIONS, inputs.get("crop_type", BASELINE)),
        ("region", REGION_OPTIONS, inputs.get("region", BASELINE)),
        ("season", SEASON_OPTIONS, inputs.get("season", BASELINE)),
    ):
        if chosen != BASELINE and chosen not in options:
            raise ValueError(f"unknown {prefix}: {chosen}")
        for opt in options:
            row[f"{prefix}_{opt}"] = 1.0 if chosen == opt else 0.0
    return {c: row[c] for c in YIELD_FEATURES}


def apply_yield_scaler(scaler, frame: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Scale with scaler.transform() ONLY (never fit).  Returns (frame, mode description).

    The scaled columns are determined from the scaler's own metadata:
      1. ``feature_names_in_`` -> exactly those columns (by name);
      2. ``n_features_in_`` == 23 -> every column;
      3. ``n_features_in_`` in (11, 13) -> the leading numeric block of the original order;
      4. anything else -> SchemaError (no guessing).
    """
    frame = frame.astype(float)
    names = getattr(scaler, "feature_names_in_", None)
    n = getattr(scaler, "n_features_in_", None)
    out = frame.copy()
    if names is not None:
        cols = [str(c) for c in names]
        missing = [c for c in cols if c not in frame.columns]
        if missing:
            raise SchemaError(f"scaler expects unknown columns: {missing}")
        out[cols] = scaler.transform(frame[cols])
        return out, f"named columns ({len(cols)})"
    if n == len(frame.columns):
        out[:] = scaler.transform(frame.values)
        return out, f"all {n} columns"
    if n in (11, 13):
        cols = list(frame.columns[:n])
        out[cols] = scaler.transform(frame[cols].values)
        return out, f"first {n} columns of the original order"
    raise SchemaError(f"cannot map a scaler with {n} features onto the {len(frame.columns)} yield features")


def predict_yield(inputs: dict[str, Any], model=None, scaler=None) -> dict:
    model = model if model is not None else get_yield_model()
    scaler = scaler if scaler is not None else get_yield_scaler()
    row = build_yield_row(inputs)
    frame = pd.DataFrame([row], columns=YIELD_FEATURES)
    scaled, mode = apply_yield_scaler(scaler, frame)
    X = _model_input(model, {c: float(scaled.iloc[0][c]) for c in YIELD_FEATURES}, YIELD_FEATURES)
    per_ha = float(np.ravel(model.predict(X))[0])
    return {
        "tons_per_hectare": per_ha,
        "tons_per_feddan": ton_per_feddan(per_ha),
        "scaler_mode": mode,
    }
