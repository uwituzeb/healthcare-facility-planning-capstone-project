# Models Directory

This directory contains trained machine learning models for the Healthcare Facility Planning system.

## Files

- `healthcare_model.pkl` - Trained Random Forest classifier + StandardScaler
- `metadata.json` - Model metadata (version, metrics, training date)

## Model Information

**Algorithm:** Random Forest Classifier
**Features:** 12 features extracted from satellite imagery patches
**Input:** 256x256 pixel satellite image patch
**Output:** Binary classification (Healthcare facility: Yes/No)

## Training

To train the model, run:

```bash
python capstoneNotebook_readable.py
```

This will:
1. Load satellite imagery from Google Earth Engine
2. Extract features from image patches
3. Train Random Forest model
4. Save model to `models/healthcare_model.pkl`

## Usage

```python
import pickle

# Load model
with open('models/healthcare_model.pkl', 'rb') as f:
    model_data = pickle.load(f)
    model = model_data['model']
    scaler = model_data['scaler']

# Make prediction
features = extract_features(image_patch)  # 12 features
features_scaled = scaler.transform([features])
prediction = model.predict(features_scaled)[0]
confidence = model.predict_proba(features_scaled)[0]
```

## Model Versioning

Models are versioned using semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes to model architecture
- MINOR: New features or improvements
- PATCH: Bug fixes or retraining with same architecture

Current version: v1.0
