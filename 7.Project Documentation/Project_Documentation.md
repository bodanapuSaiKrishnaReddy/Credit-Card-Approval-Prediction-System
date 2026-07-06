# Phase 7: Project Documentation

## 🚀 Getting Started

### 📋 Prerequisites
Install Python 3.8+ and dependencies:
```bash
pip install flask pandas numpy scikit-learn pydantic
```

### 🏋️ Model Training
To train the Random Forest predictor model from the raw CSV records inside `archive/` directory:
```bash
python pipeline.py
```
This saves `model.pkl`, `scaler.pkl`, and `encoders.pkl` assets.

### 💻 Running the Web Application
Start the Flask application server:
```bash
python app.py
```
Open a browser and navigate to `http://127.0.0.1:5000` to start assessments.
