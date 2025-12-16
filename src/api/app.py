"""
Production-ready Flask API with logging, validation, and monitoring
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError, Field
from typing import Optional
import time
from src.predict import ChurnPredictor
from src.logger import setup_logger
from config import config

# Initialize app
app = Flask(__name__)
CORS(app)

# Setup logger
logger = setup_logger(__name__)

# Initialize predictor (load model once)
try:
    predictor = ChurnPredictor()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    predictor = None

# Metrics
metrics = {
    'total_requests': 0,
    'successful_predictions': 0,
    'failed_predictions': 0,
    'errors': 0
}


# Pydantic model for input validation
class CustomerInput(BaseModel):
    age: int = Field(..., ge=18, le=100)
    tenure_months: int = Field(..., ge=0, le=120)
    monthly_charges: float = Field(..., ge=0, le=1000)
    total_charges: float = Field(..., ge=0)
    support_tickets: int = Field(..., ge=0, le=100)
    login_frequency: int = Field(..., ge=0, le=1000)
    feature_usage: float = Field(..., ge=0, le=1)
    gender_encoded: int = Field(..., ge=0, le=1)
    location_encoded: int = Field(..., ge=0, le=2)
    contract_type_encoded: int = Field(..., ge=0, le=2)
    internet_service_encoded: int = Field(..., ge=0, le=2)
    payment_method_encoded: int = Field(..., ge=0, le=2)
    charges_per_month: float = Field(..., ge=0)
    support_per_month: float = Field(..., ge=0)
    login_per_month: float = Field(..., ge=0)
    is_new_customer: int = Field(..., ge=0, le=1)
    is_high_value: int = Field(..., ge=0, le=1)
    has_tech_support: int = Field(..., ge=0, le=1)
    has_device_protection: int = Field(..., ge=0, le=1)
    tenure_charges_interaction: float = Field(..., ge=0)
    support_value_ratio: float = Field(..., ge=0)


@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'Customer Churn Prediction API',
        'version': config.MODEL_VERSION,
        'api_version': config.API_VERSION,
        'endpoints': {
            'predict': f'/api/{config.API_VERSION}/predict',
            'health': '/health',
            'ready': '/ready',
            'metrics': '/metrics'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    }), 200


@app.route('/ready')
def ready():
    """Readiness check endpoint"""
    if predictor is None or not predictor.is_ready():
        return jsonify({
            'status': 'not ready',
            'reason': 'Model not loaded'
        }), 503
    
    return jsonify({
        'status': 'ready',
        'model_version': config.MODEL_VERSION
    }), 200


@app.route('/metrics')
def get_metrics():
    """Return API metrics"""
    if not config.ENABLE_METRICS:
        return jsonify({'error': 'Metrics disabled'}), 403
    
    return jsonify(metrics), 200


@app.route(f'/api/{config.API_VERSION}/predict', methods=['POST'])
def predict():
    """Predict customer churn"""
    
    metrics['total_requests'] += 1
    
    # Check if model is loaded
    if predictor is None or not predictor.is_ready():
        metrics['errors'] += 1
        logger.error("Model not loaded")
        return jsonify({
            'success': False,
            'error': 'Model not available'
        }), 503
    
    # Validate input
    try:
        customer_data = CustomerInput(**request.get_json())
    except ValidationError as e:
        metrics['failed_predictions'] += 1
        logger.warning(f"Validation error: {e}")
        return jsonify({
            'success': False,
            'error': 'Invalid input',
            'details': e.errors()
        }), 400
    except Exception as e:
        metrics['errors'] += 1
        logger.error(f"Input error: {e}")
        return jsonify({
            'success': False,
            'error': 'Invalid request format'
        }), 400
    
    # Make prediction
    try:
        result = predictor.predict(customer_data.dict())
        metrics['successful_predictions'] += 1
        
        logger.info(f"Prediction successful: {result['churn_prediction']}")
        
        return jsonify({
            'success': True,
            'model_version': config.MODEL_VERSION,
            'result': result
        }), 200
    
    except Exception as e:
        metrics['failed_predictions'] += 1
        logger.error(f"Prediction error: {e}")
        return jsonify({
            'success': False,
            'error': 'Prediction failed'
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    metrics['errors'] += 1
    logger.error(f"Internal error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Only for development - use Gunicorn in production
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
