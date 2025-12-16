# 📊 Customer Churn Prediction System

A machine learning system that predicts customer churn using XGBoost with feature engineering and SMOTE for class imbalance handling.

---

## 📋 Project Overview

This system analyzes customer behavior to predict churn probability. It processes customer demographics, usage patterns, and transaction history through a feature engineering pipeline to identify at-risk customers.

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **XGBoost** - Gradient boosting classifier
- **Scikit-learn** - ML utilities
- **Pandas & NumPy** - Data processing
- **SMOTE** - Class imbalance handling
- **Flask** - REST API
- **Gunicorn** - Production server
- **Docker** - Containerization
- **Pydantic** - Input validation

---

## 🧠 How It Works

The system uses XGBoost to classify customers as likely to churn or not. Customer data goes through feature engineering to create meaningful features like usage ratios and behavioral indicators. SMOTE balances the training dataset. The trained model outputs churn probability scores through a REST API.

---

## 📁 Project Structure

```
customer-churn-prediction/
├── README.md
├── requirements.txt
├── .env
├── config.py
├── Dockerfile
│
├── src/
│   ├── logger.py
│   ├── data_loader.py
│   ├── feature_engineering.py
│   ├── model.py
│   ├── train.py
│   └── predict.py
│
├── api/
│   └── app.py
│
├── tests/
│   └── test_api.py
│
└── logs/
```

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/rahulkumar/customer-churn-prediction.git
cd customer-churn-prediction
pip install -r requirements.txt
```

### Environment Setup

Create `.env` file:
```env
FLASK_ENV=production
MODEL_PATH=models/churn_model.pkl
PORT=5000
```

### Train Model

```bash
python src/train.py
```

### Run API

**Development:**
```bash
python api/app.py
```

**Production:**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 api.app:app
```

### Docker

```bash
# Build
docker build -t churn-predictor .

# Run
docker run -p 5000:5000 churn-predictor

# Check health
curl http://localhost:5000/health
```

---

## ✨ Key Features

- **XGBoost Classifier** - Optimized gradient boosting
- **Feature Engineering** - Automated feature creation
- **SMOTE** - Handles class imbalance
- **Input Validation** - Pydantic schemas
- **Production API** - Gunicorn with health checks
- **Logging** - Structured logs with file rotation
- **Monitoring** - Request and error metrics
- **Testing** - Unit tests included
- **Docker Ready** - Multi-stage build

---

## 📊 Model Details


**Model Configuration:**
- Algorithm: XGBoost
- Max depth: 6
- Learning rate: 0.1
- Estimators: 200

---

## 🌐 API Endpoints

### Health Check
```bash
GET /health
```

### Readiness Check
```bash
GET /ready
```

### Metrics
```bash
GET /metrics
```

### Prediction
```bash
POST /api/v1/predict
Content-Type: application/json

{
  "age": 35,
  "tenure_months": 12,
  "monthly_charges": 65.0,
  ...
}

Response:
{
  "success": true,
  "model_version": "1.0.0",
  "result": {
    "churn_prediction": 0,
    "churn_probability": 0.23,
    "risk_level": "Low"
  }
}
```

---

## 🔧 Configuration

All configuration via environment variables in `.env`:

```env
# Application
FLASK_ENV=production
DEBUG=False
LOG_LEVEL=INFO

# Model
MODEL_PATH=models/churn_model.pkl
MODEL_VERSION=1.0.0

# API
API_VERSION=v1
PORT=5000
WORKERS=4
```

---

## 🧪 Testing

```bash
# Run tests
python tests/test_api.py

# With pytest
pip install pytest
pytest tests/
```

---

## 📝 Development

### Add New Features

1. Update `src/feature_engineering.py`
2. Retrain model with `src/train.py`
3. Update input schema in `api/app.py`

### Logging

Logs saved to `logs/app_YYYYMMDD.log`

```python
from src.logger import setup_logger
logger = setup_logger(__name__)
logger.info("Message")
```

---

## 🐳 Docker Deployment

**Build:**
```bash
docker build -t churn-predictor:v1 .
```

**Run:**
```bash
docker run -d \
  -p 5000:5000 \
  --name churn-api \
  --env-file .env \
  churn-predictor:v1
```

**Logs:**
```bash
docker logs churn-api
```

**Stop:**
```bash
docker stop churn-api
docker rm churn-api
```

---

## 🔮 Future Improvements

- Add more algorithms for comparison
- Implement online learning
- Add feature importance visualization
- Build interactive dashboard
- Add model versioning system

---

## 📄 License

MIT License - Open source and free to use
