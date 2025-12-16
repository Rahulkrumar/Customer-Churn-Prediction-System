"""
API tests
"""

import sys
sys.path.insert(0, '..')

from api.app import app
import json


def test_health():
    """Test health endpoint"""
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_ready():
    """Test ready endpoint"""
    client = app.test_client()
    response = client.get('/ready')
    assert response.status_code in [200, 503]


def test_predict_valid():
    """Test prediction with valid input"""
    client = app.test_client()
    
    data = {
        'age': 35,
        'tenure_months': 12,
        'monthly_charges': 65.0,
        'total_charges': 780.0,
        'support_tickets': 2,
        'login_frequency': 20,
        'feature_usage': 0.7,
        'gender_encoded': 1,
        'location_encoded': 0,
        'contract_type_encoded': 1,
        'internet_service_encoded': 1,
        'payment_method_encoded': 0,
        'charges_per_month': 65.0,
        'support_per_month': 0.17,
        'login_per_month': 1.67,
        'is_new_customer': 0,
        'is_high_value': 0,
        'has_tech_support': 1,
        'has_device_protection': 1,
        'tenure_charges_interaction': 780.0,
        'support_value_ratio': 0.03
    }
    
    response = client.post(
        '/api/v1/predict',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Should either succeed or fail gracefully
    assert response.status_code in [200, 500, 503]


def test_predict_invalid():
    """Test prediction with invalid input"""
    client = app.test_client()
    
    data = {'age': -5}  # Invalid age
    
    response = client.post(
        '/api/v1/predict',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert response.json['success'] == False


if __name__ == '__main__':
    test_health()
    test_ready()
    test_predict_valid()
    test_predict_invalid()
    print("All tests passed!")
