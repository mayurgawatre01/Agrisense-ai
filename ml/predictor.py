"""
CropSense v2.0 — ML Predictor Module
"""
import joblib
import os
import logging
import hashlib
import json
import numpy as np

logger = logging.getLogger(__name__)

MODEL_PATH   = os.path.join(os.path.dirname(__file__), 'model.pkl')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'encoders.pkl')

_PREDICTION_CACHE: dict = {}


def _cache_key(data: dict) -> str:
    stable = json.dumps({k: data[k] for k in sorted(data)}, sort_keys=True)
    return hashlib.md5(stable.encode()).hexdigest()


def predict_yield(data: dict) -> dict:
    required = {'state', 'season', 'crop', 'area'}
    missing = required - set(data.keys())
    if missing:
        return {'success': False, 'error': f"Missing fields: {', '.join(missing)}"}

    try:
        area = float(data['area'])
        if area <= 0:
            return {'success': False, 'error': 'Area must be greater than 0.'}
    except (TypeError, ValueError):
        return {'success': False, 'error': 'Invalid area value.'}

    key = _cache_key(data)
    if key in _PREDICTION_CACHE:
        return _PREDICTION_CACHE[key]

    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
            result = _ml_predict(data)
        else:
            result = _rule_based_predict(data)
    except Exception as exc:
        logger.exception("Prediction failed: %s", exc)
        result = {'success': False, 'error': f"Prediction error: {str(exc)}"}

    if result.get('success'):
        _PREDICTION_CACHE[key] = result

    return result


def _ml_predict(data: dict) -> dict:
    model    = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODER_PATH)

    def safe_encode(enc, value):
        return int(enc.transform([value])[0]) if value in enc.classes_ else 0

    state_enc  = safe_encode(encoders['state'],  data['state'])
    season_enc = safe_encode(encoders['season'], data['season'])
    crop_enc   = safe_encode(encoders['crop'],   data['crop'])
    area       = float(data['area'])

    features  = np.array([[state_enc, season_enc, crop_enc, area]])
    predicted = float(model.predict(features)[0])
    confidence = _estimate_confidence(model, features, predicted)

    return {
        'success':          True,
        'predicted_yield':  round(predicted, 2),
        'confidence':       round(confidence, 2),
        'total_production': round(predicted * area, 2),
        'model_used':       'Random Forest (ML)',
        'input':            data,
    }


def _estimate_confidence(model, features, predicted: float) -> float:
    try:
        tree_preds = np.array([t.predict(features)[0] for t in model.estimators_])
        std = float(np.std(tree_preds))
        return max(0.60, min(0.95, 0.95 - std * 0.06))
    except Exception:
        return min(0.92, max(0.65, 1 - abs(predicted - 2.5) / 10))


def _rule_based_predict(data: dict) -> dict:
    base_yields = {
        'Rice': 2.5, 'Wheat': 3.1, 'Maize': 2.8, 'Cotton': 1.2,
        'Sugarcane': 65.0, 'Groundnut': 1.4, 'Soyabean': 1.1,
        'Sunflower': 0.9, 'Banana': 28.0, 'Potato': 22.0,
        'Tomato': 20.0, 'Onion': 18.0, 'Bajra': 1.0, 'Jowar': 1.2,
        'Pulses': 0.8, 'Mango': 8.0, 'Other': 2.0,
    }
    season_mult = {
        'Kharif': 1.00, 'Rabi': 1.05, 'Whole Year': 0.95,
        'Summer': 0.85, 'Winter': 1.10, 'Autumn': 0.90,
    }
    state_mult = {
        'Punjab': 1.15, 'Haryana': 1.10, 'Uttar Pradesh': 1.05,
        'Maharashtra': 1.00, 'Karnataka': 0.97, 'Bihar': 0.92,
    }

    crop      = data['crop']
    area      = float(data['area'])
    base      = base_yields.get(crop, 2.0)
    s_mult    = season_mult.get(data['season'], 1.0)
    st_mul    = state_mult.get(data['state'], 1.0)
    noise     = float(np.random.uniform(0.92, 1.08))
    predicted = base * s_mult * st_mul * noise

    return {
        'success':          True,
        'predicted_yield':  round(predicted, 2),
        'confidence':       0.68,
        'total_production': round(predicted * area, 2),
        'model_used':       'Rule-Based (upload data & train ML for higher accuracy)',
        'input':            data,
    }


def model_status() -> dict:
    if os.path.exists(MODEL_PATH):
        return {
            'trained':      True,
            'size_kb':      os.path.getsize(MODEL_PATH) // 1024,
            'last_trained': os.path.getmtime(MODEL_PATH),
        }
    return {'trained': False}


def clear_cache() -> None:
    global _PREDICTION_CACHE
    _PREDICTION_CACHE.clear()
