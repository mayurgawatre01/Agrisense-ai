"""
CropSense v2.0 — Model Training Script
Run after uploading CSV data to retrain the Random Forest model.

Usage:
    python ml/train_model.py
    python ml/train_model.py --min-rows 50
"""
import argparse
import logging
import os
import sys
import time

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

ML_DIR       = os.path.dirname(__file__)
MODEL_PATH   = os.path.join(ML_DIR, 'model.pkl')
ENCODER_PATH = os.path.join(ML_DIR, 'encoders.pkl')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(levelname)-8s  %(message)s',
    datefmt='%H:%M:%S',
)
logger = logging.getLogger('train')


def fetch_data(min_rows: int) -> pd.DataFrame:
    """Fetch crop data from SQLite via Flask-SQLAlchemy."""
    # FIX: original used mysql.connection — replaced with SQLAlchemy (SQLite)
    from app import create_app, db
    from models import CropData

    app = create_app()
    with app.app_context():
        rows = db.session.query(
            CropData.state, CropData.season, CropData.crop,
            CropData.area, CropData.yield_per_hectare
        ).filter(
            CropData.yield_per_hectare > 0,
            CropData.area > 0
        ).all()

    if len(rows) < min_rows:
        logger.error("Not enough data (%d rows). Upload more CSV data first (need >= %d).", len(rows), min_rows)
        sys.exit(1)

    df = pd.DataFrame(rows, columns=['state', 'season', 'crop', 'area', 'yield_per_hectare'])
    logger.info("Fetched %d records from database.", len(df))
    return df


def preprocess(df: pd.DataFrame):
    encoders: dict = {}
    for col in ['state', 'season', 'crop']:
        le = LabelEncoder()
        df[col + '_enc'] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
        logger.info("  %s: %d unique values", col, len(le.classes_))

    y = df['yield_per_hectare'].values
    q_lo, q_hi = np.percentile(y, [5, 95])
    mask = (y >= q_lo) & (y <= q_hi)
    df = df[mask].copy()
    logger.info("After outlier removal: %d rows (removed %d)", len(df), (~mask).sum())

    X = df[['state_enc', 'season_enc', 'crop_enc', 'area']].values
    y = df['yield_per_hectare'].values
    return X, y, encoders


def train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(
        n_estimators=300, max_depth=14,
        min_samples_split=4, min_samples_leaf=2,
        max_features='sqrt', random_state=42, n_jobs=-1,
    )

    logger.info("Training Random Forest (300 trees)...")
    t0 = time.time()
    model.fit(X_train, y_train)
    logger.info("Training complete in %.1f s", time.time() - t0)

    y_pred = model.predict(X_test)
    r2   = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae  = mean_absolute_error(y_test, y_pred)
    logger.info("Test-set  -> R2: %.4f | RMSE: %.4f | MAE: %.4f", r2, rmse, mae)

    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring='r2', n_jobs=-1)
    logger.info("5-fold CV -> R2: %.4f +/- %.4f", cv_scores.mean(), cv_scores.std())

    return model, {'r2': round(r2, 4), 'rmse': round(rmse, 4), 'mae': round(mae, 4)}


def save_artifacts(model, encoders):
    joblib.dump(model, MODEL_PATH, compress=3)
    joblib.dump(encoders, ENCODER_PATH, compress=3)
    logger.info("Model saved -> %s (%d KB)", MODEL_PATH, os.path.getsize(MODEL_PATH) // 1024)
    logger.info("Encoders saved -> %s", ENCODER_PATH)


def main():
    parser = argparse.ArgumentParser(description='CropSense model trainer')
    parser.add_argument('--min-rows', type=int, default=100)
    args = parser.parse_args()

    logger.info("=" * 50)
    logger.info("CropSense v2.0 — Model Training")
    logger.info("=" * 50)

    df = fetch_data(args.min_rows)
    X, y, encoders = preprocess(df)
    model, metrics = train(X, y)
    save_artifacts(model, encoders)

    try:
        from ml.predictor import clear_cache
        clear_cache()
        logger.info("Prediction cache cleared.")
    except ImportError:
        pass

    logger.info("Done! R2 = %.4f | RMSE = %.4f t/ha", metrics['r2'], metrics['rmse'])
    logger.info("Restart Flask app — new model will be used automatically.")


if __name__ == '__main__':
    main()
