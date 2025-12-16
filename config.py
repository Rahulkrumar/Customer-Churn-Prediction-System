"""
Configuration management with environment variables
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # Application
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Model
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/churn_model.pkl')
    MODEL_VERSION = os.getenv('MODEL_VERSION', '1.0.0')
    
    # API
    API_VERSION = os.getenv('API_VERSION', 'v1')
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    WORKERS = int(os.getenv('WORKERS', 4))
    
    # Monitoring
    ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'True').lower() == 'true'
    
    # Data
    N_CUSTOMERS = 10000
    N_FEATURES = 25
    
    # Model Training
    MAX_DEPTH = 6
    LEARNING_RATE = 0.1
    N_ESTIMATORS = 200
    SUBSAMPLE = 0.8
    COLSAMPLE_BYTREE = 0.8
    
    # SMOTE
    SMOTE_SAMPLING_STRATEGY = 0.8
    SMOTE_K_NEIGHBORS = 5
    
    # Training
    TEST_SIZE = 0.2
    RANDOM_STATE = 42


config = Config()
