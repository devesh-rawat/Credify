import joblib
import pandas as pd
import numpy as np
import os
from core.config import settings

class MLService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()

    def load_model(self):
        """Loads the ML model and scaler from disk."""
        try:
            # Construct absolute paths
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, settings.ML_MODEL_PATH)
            scaler_path = os.path.join(base_dir, settings.SCALER_PATH)
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                print(f"ML Model loaded from {model_path}")
            else:
                print(f"ML Model not found at {model_path} or {scaler_path}. Using dummy logic.")
        except Exception as e:
            print(f"Error loading ML model: {e}")

    def predict_score(self, features: dict) -> dict:
        """
        Predicts credit score and default probability based on features.
        """
        if self.model and self.scaler:
            try:
                # Base features
                TOP_FEATURES = [
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
                
                # Create DataFrame with base features
                input_data = {k: [features.get(k, 0)] for k in TOP_FEATURES}
                df = pd.DataFrame(input_data)
                
                # Apply same feature engineering as training
                df['DEBT_SAVINGS_INTERACTION'] = df['DEBT'] * df['SAVINGS']
                df['DEBT_INCOME_SQUARED'] = df['R_DEBT_INCOME'] ** 2
                df['SAVINGS_INCOME_SQUARED'] = df['R_SAVINGS_INCOME'] ** 2
                df['HIGH_RISK_SPENDING'] = (df['R_GAMBLING_INCOME'] + df['R_ENTERTAINMENT_INCOME']) / 2
                df['FINANCIAL_STABILITY'] = df['R_SAVINGS_INCOME'] - df['R_DEBT_INCOME']
                
                # Scale
                X_scaled = self.scaler.transform(df)
                
                # Predict
                score = self.model.predict(X_scaled)[0]
                
                # Ensure score is within valid range
                score = max(300, min(900, score))
                
                # Default probability based on score
                default_prob = max(0, min(1, (900 - score) / 600))
                
                return {
                    "credit_score": int(score),
                    "default_probability": float(default_prob),
                    "risk_label": "Low" if score > 700 else "Medium" if score > 600 else "High"
                }
            except Exception as e:
                print(f"Prediction error: {e}")
                return self._dummy_prediction()
        else:
            return self._dummy_prediction()

    def _dummy_prediction(self):
        return {
            "credit_score": 750,
            "default_probability": 0.05,
            "risk_label": "Low"
        }

    def predict(self, features: dict) -> dict:
        return self.predict_score(features)

ml_service = MLService()
