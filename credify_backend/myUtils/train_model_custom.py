"""
CUSTOMIZABLE CREDIT SCORE MODEL TRAINING SCRIPT

This script allows you to train the credit score model with your own parameters.
You can modify:
1. Training data (load from CSV or generate synthetic)
2. Model hyperparameters
3. Feature engineering
4. Train-test split ratio
5. Model type (RandomForest, GradientBoosting, XGBoost, etc.)

Author: AI Assistant
Date: 2025-11-24
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import joblib
from datetime import datetime

# ============================================================================
# CONFIGURATION - MODIFY THESE PARAMETERS AS NEEDED
# ============================================================================

# Data source: 'csv' to load from CSV, 'synthetic' to generate new data
DATA_SOURCE = 'csv'  # Change to 'synthetic' to regenerate data
CSV_FILE = 'training_data.csv'  # Path to your training data CSV

# Model selection: 'random_forest', 'gradient_boosting'
MODEL_TYPE = 'random_forest'

# Train-test split
TEST_SIZE = 0.2  # 20% for testing
RANDOM_STATE = 42  # For reproducibility

# RandomForest hyperparameters (modify these to tune the model)
RF_PARAMS = {
    'n_estimators': 200,        # Number of trees (more = better but slower)
    'max_depth': 20,            # Maximum depth of trees (None = unlimited)
    'min_samples_split': 5,     # Minimum samples to split a node
    'min_samples_leaf': 2,      # Minimum samples in a leaf
    'max_features': 'sqrt',     # Features to consider for best split
    'random_state': RANDOM_STATE,
    'n_jobs': -1,               # Use all CPU cores
    'verbose': 1                # Show progress
}

# GradientBoosting hyperparameters (alternative model)
GB_PARAMS = {
    'n_estimators': 200,
    'max_depth': 5,
    'learning_rate': 0.1,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': RANDOM_STATE,
    'verbose': 1
}

# Feature engineering flags
APPLY_FEATURE_ENGINEERING = True  # Add interaction features

# Output paths
MODEL_PATH = 'ml_models/credit_score_model.pkl'
SCALER_PATH = 'ml_models/scaler.pkl'
METADATA_PATH = 'ml_models/model_metadata.pkl'

# ============================================================================
# FEATURE DEFINITIONS
# ============================================================================

# These are the base features used by the ML service
# DO NOT MODIFY unless you also update ml_service.py
BASE_FEATURES = [
    'R_DEBT_INCOME', 'R_DEBT_SAVINGS', 'DEFAULT', 'DEBT', 'R_EXPENDITURE_DEBT',
    'R_UTILITIES_DEBT', 'R_EDUCATION_INCOME', 'R_GROCERIES_DEBT', 'R_TAX_DEBT',
    'R_ENTERTAINMENT_DEBT', 'R_HEALTH_DEBT', 'R_SAVINGS_INCOME', 'R_CLOTHING_DEBT',
    'R_TRAVEL_DEBT', 'CAT_CREDIT_CARD', 'R_HOUSING_DEBT', 'R_UTILITIES_SAVINGS',
    'R_EDUCATION_SAVINGS', 'CAT_DEBT', 'R_HEALTH_SAVINGS', 'R_GROCERIES_SAVINGS',
    'R_GROCERIES_INCOME', 'R_EXPENDITURE', 'R_ENTERTAINMENT_INCOME', 'R_HEALTH_INCOME',
    'R_GAMBLING_INCOME', 'CAT_DEPENDENTS', 'R_ENTERTAINMENT', 'R_HOUSING_SAVINGS',
    'CAT_SAVINGS_ACCOUNT', 'R_TRAVEL', 'R_GROCERIES', 'R_EDUCATION_DEBT',
    'R_GAMBLING_DEBT', 'T_ENTERTAINMENT_12', 'T_EDUCATION_12', 'T_EDUCATION_6',
    'R_CLOTHING_SAVINGS', 'R_HEALTH', 'T_ENTERTAINMENT_6', 'T_GROCERIES_6',
    'R_GAMBLING_SAVINGS', 'SAVINGS', 'T_GAMBLING_6', 'T_GAMBLING_12'
]

# ============================================================================
# FUNCTIONS
# ============================================================================

def load_data_from_csv(csv_path):
    """Load training data from CSV file"""
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Separate features and target
    y = df['TARGET_SCORE'].values
    X = df.drop('TARGET_SCORE', axis=1)
    
    # Select only BASE_FEATURES
    X = X[[f for f in BASE_FEATURES if f in X.columns]]
    
    # Fill any missing features with 0
    for feature in BASE_FEATURES:
        if feature not in X.columns:
            X[feature] = 0
    
    # Reorder to match BASE_FEATURES
    X = X[BASE_FEATURES]
    
    print(f"  Loaded {len(X)} samples")
    print(f"  Features: {len(BASE_FEATURES)}")
    print(f"  Score range: {y.min():.0f} - {y.max():.0f}")
    
    return X, y

def generate_synthetic_data(samples_per_range=150):
    """Generate synthetic training data"""
    print("Generating synthetic data...")
    # Import the export script's function
    import sys
    sys.path.append('.')
    from export_training_data import export_training_data_to_csv
    
    df = export_training_data_to_csv(samples_per_range)
    
    y = df['TARGET_SCORE'].values
    X = df.drop('TARGET_SCORE', axis=1)
    
    # Select only BASE_FEATURES
    X = X[[f for f in BASE_FEATURES if f in X.columns]]
    
    # Fill any missing features with 0
    for feature in BASE_FEATURES:
        if feature not in X.columns:
            X[feature] = 0
    
    # Reorder to match BASE_FEATURES
    X = X[BASE_FEATURES]
    
    return X, y

def apply_feature_engineering(X):
    """
    Apply feature engineering transformations.
    These must match the transformations in ml_service.py
    """
    X_eng = X.copy()
    
    # Interaction features
    X_eng['DEBT_SAVINGS_INTERACTION'] = X_eng['DEBT'] * X_eng['SAVINGS']
    X_eng['DEBT_INCOME_SQUARED'] = X_eng['R_DEBT_INCOME'] ** 2
    X_eng['SAVINGS_INCOME_SQUARED'] = X_eng['R_SAVINGS_INCOME'] ** 2
    X_eng['HIGH_RISK_SPENDING'] = (X_eng['R_GAMBLING_INCOME'] + X_eng['R_ENTERTAINMENT_INCOME']) / 2
    X_eng['FINANCIAL_STABILITY'] = X_eng['R_SAVINGS_INCOME'] - X_eng['R_DEBT_INCOME']
    
    return X_eng

def create_model(model_type):
    """Create and return the specified model"""
    if model_type == 'random_forest':
        print(f"\nCreating RandomForest model with parameters:")
        for key, value in RF_PARAMS.items():
            print(f"  {key}: {value}")
        return RandomForestRegressor(**RF_PARAMS)
    
    elif model_type == 'gradient_boosting':
        print(f"\nCreating GradientBoosting model with parameters:")
        for key, value in GB_PARAMS.items():
            print(f"  {key}: {value}")
        return GradientBoostingRegressor(**GB_PARAMS)
    
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def evaluate_model(model, X, y, dataset_name="Dataset"):
    """Evaluate model performance"""
    y_pred = model.predict(X)
    y_pred = np.clip(y_pred, 300, 900)  # Clip to valid range
    
    mae = mean_absolute_error(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    r2 = r2_score(y, y_pred)
    
    print(f"\n{dataset_name} Performance:")
    print(f"  MAE:  {mae:.2f} points")
    print(f"  RMSE: {rmse:.2f} points")
    print(f"  R²:   {r2:.4f}")
    print(f"  Score range: {y_pred.min():.0f} - {y_pred.max():.0f}")
    
    return {'mae': mae, 'rmse': rmse, 'r2': r2}

def save_model_artifacts(model, scaler, metadata):
    """Save model, scaler, and metadata"""
    print("\nSaving model artifacts...")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(metadata, METADATA_PATH)
    
    print(f"  ✓ Model saved to: {MODEL_PATH}")
    print(f"  ✓ Scaler saved to: {SCALER_PATH}")
    print(f"  ✓ Metadata saved to: {METADATA_PATH}")

# ============================================================================
# MAIN TRAINING PIPELINE
# ============================================================================

def train_model():
    """Main training pipeline"""
    print("=" * 80)
    print("CREDIT SCORE MODEL TRAINING")
    print("=" * 80)
    
    # Step 1: Load data
    if DATA_SOURCE == 'csv':
        X, y = load_data_from_csv(CSV_FILE)
    else:
        X, y = generate_synthetic_data()
    
    print(f"\nDataset Statistics:")
    print(f"  Total samples: {len(X)}")
    print(f"  Features: {len(BASE_FEATURES)}")
    print(f"  Score distribution:")
    print(f"    Min:  {y.min():.0f}")
    print(f"    Max:  {y.max():.0f}")
    print(f"    Mean: {y.mean():.2f}")
    print(f"    Std:  {y.std():.2f}")
    
    # Step 2: Apply feature engineering
    if APPLY_FEATURE_ENGINEERING:
        print("\nApplying feature engineering...")
        X = apply_feature_engineering(X)
        print(f"  Features after engineering: {X.shape[1]}")
    
    # Step 3: Split data
    print(f"\nSplitting data (test size: {TEST_SIZE})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    print(f"  Training samples: {len(X_train)}")
    print(f"  Test samples: {len(X_test)}")
    
    # Step 4: Scale features
    print("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Step 5: Train model
    print("\nTraining model...")
    model = create_model(MODEL_TYPE)
    model.fit(X_train_scaled, y_train)
    
    # Step 6: Evaluate
    train_metrics = evaluate_model(model, X_train_scaled, y_train, "Training")
    test_metrics = evaluate_model(model, X_test_scaled, y_test, "Test")
    
    # Step 7: Feature importance (for tree-based models)
    if hasattr(model, 'feature_importances_'):
        print("\nTop 10 Most Important Features:")
        importances = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for idx, row in importances.head(10).iterrows():
            print(f"  {row['feature']:<30} {row['importance']:.4f}")
    
    # Step 8: Save artifacts
    metadata = {
        'model_type': MODEL_TYPE,
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'train_mae': float(train_metrics['mae']),
        'test_mae': float(test_metrics['mae']),
        'train_r2': float(train_metrics['r2']),
        'test_r2': float(test_metrics['r2']),
        'feature_count': X.shape[1],
        'base_features': len(BASE_FEATURES),
        'trained_at': datetime.now().isoformat(),
        'hyperparameters': RF_PARAMS if MODEL_TYPE == 'random_forest' else GB_PARAMS
    }
    
    save_model_artifacts(model, scaler, metadata)
    
    print("\n" + "=" * 80)
    print("✓ TRAINING COMPLETE!")
    print("=" * 80)
    
    return model, scaler, metadata

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Run training
    model, scaler, metadata = train_model()
    
    print("\nTo use this model:")
    print("1. The model is already saved and will be used by the backend")
    print("2. To modify training, edit the CONFIGURATION section above")
    print("3. To use custom data, create a CSV with the required features")
    print("4. Run this script again to retrain with new parameters")
