"""
Prediction module with singleton pattern for model loading
"""

import pandas as pd
from src.model import load_model
from src.logger import setup_logger
from config import config

logger = setup_logger(__name__)


class ChurnPredictor:
    """Singleton predictor class"""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_model()
        return cls._instance
    
    def _load_model(self):
        """Load model once"""
        try:
            self._model = load_model(config.MODEL_PATH)
            logger.info(f"Model loaded from {config.MODEL_PATH}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self._model = None
    
    def is_ready(self):
        """Check if model is ready"""
        return self._model is not None
    
    def predict(self, customer_data):
        """
        Predict churn probability
        
        Args:
            customer_data: dict with customer features
        
        Returns:
            dict with prediction results
        """
        
        if not self.is_ready():
            raise RuntimeError("Model not loaded")
        
        # Convert to DataFrame
        df = pd.DataFrame([customer_data])
        
        # Predict
        churn_prob = self._model.predict_proba(df)[:, 1][0]
        churn_pred = 1 if churn_prob > 0.5 else 0
        
        return {
            'churn_prediction': int(churn_pred),
            'churn_probability': float(round(churn_prob, 4)),
            'risk_level': 'High' if churn_prob > 0.7 else 'Medium' if churn_prob > 0.4 else 'Low'
        }
