"""
Export Best Model Script
Trains the best performing ML model on the full features dataset
and saves the trained model pipeline to model_dev/model.pkl.
"""

import os
import shutil
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.svm import SVR
from color_service import extract_color_features


def export_model():
    base_dev_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dev_dir, 'data')
    features_csv = os.path.join(data_dir, 'features.csv')

    if not os.path.exists(features_csv):
        print(f"Error: {features_csv} not found. Run build_features.py first.")
        return

    df = pd.read_csv(features_csv)
    feature_cols = ['r', 'g', 'b', 'l', 'a', 'b_lab']
    X = df[feature_cols].values
    y = df['fan_score'].values

    # Train best model pipeline (SVR achieved highest R^2 = 0.9004)
    best_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', SVR(kernel='rbf', C=10.0, epsilon=0.1))
    ])

    print("Fitting model on full dataset...")
    best_pipeline.fit(X, y)

    model_path = os.path.join(base_dev_dir, 'model.pkl')
    joblib.dump(best_pipeline, model_path)
    print(f"Successfully saved best model to: {model_path}")

    # Copy to egg_api/model/model.pkl if directory exists
    api_model_dir = os.path.abspath(os.path.join(base_dev_dir, '..', 'egg_api', 'model'))
    if os.path.exists(os.path.dirname(api_model_dir)):
        os.makedirs(api_model_dir, exist_ok=True)
        api_model_path = os.path.join(api_model_dir, 'model.pkl')
        shutil.copy2(model_path, api_model_path)
        print(f"Copied model to API: {api_model_path}")

    # Sanity Test
    sample_input = [[226.0, 131.0, 23.0, 64.2, 29.8, 65.9]]
    raw_pred = best_pipeline.predict(sample_input)[0]
    rounded_score = int(round(np.clip(raw_pred, 1, 15))) if 'np' in globals() else int(round(max(1, min(15, raw_pred))))
    print(f"\n[Sanity Check]")
    print(f"Sample Input (RGB=[226,131,23], CIELAB=[64.2, 29.8, 65.9])")
    print(f"Raw Score: {raw_pred:.2f} -> Rounded Score: {rounded_score}")


if __name__ == '__main__':
    export_model()
