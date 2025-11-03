"""
Enhanced Flask API for Healthcare Facility Planning

This improved version includes:
- Real ML model integration
- LLM-powered insights
- HSSP V compliance checking
- Database integration (ready for Supabase)
- Better error handling

Author: Healthcare Facility Planning Team
Date: 2025-11-03
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Import our custom modules
from llm_analysis import LLMAnalyzer, analyze_with_llm

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURATION
# =============================================================================

class Config:
    """Application configuration"""
    # Model paths
    MODEL_PATH = Path(__file__).parent / 'models' / 'healthcare_model.pkl'

    # HSSP V Targets (Rwanda Health Sector Strategic Plan)
    HSSP_TARGET_TRAVEL_TIME = int(os.getenv('HSSP_TARGET_TRAVEL_TIME', 25))  # WHO standard
    HSSP_TARGET_COVERAGE = int(os.getenv('HSSP_TARGET_COVERAGE', 95))  # percentage
    HSSP_TARGET_FACILITY_DENSITY = int(os.getenv('HSSP_TARGET_FACILITY_DENSITY', 5))  # per 10k people

    # LLM Configuration
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')

    # Database (Supabase)
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')


# =============================================================================
# ML MODEL LOADING
# =============================================================================

def load_ml_model():
    """Load trained ML model and scaler"""
    try:
        if not Config.MODEL_PATH.exists():
            logger.warning(f"Model file not found at {Config.MODEL_PATH}")
            logger.warning("Run: python capstoneNotebook_readable.py to train the model")
            return None, None

        with open(Config.MODEL_PATH, 'rb') as f:
            model_data = pickle.load(f)
            model = model_data['model']
            scaler = model_data['scaler']

        logger.info(f"✅ ML Model loaded successfully from {Config.MODEL_PATH}")
        return model, scaler

    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        return None, None


# Load model at startup
ml_model, ml_scaler = load_ml_model()

# Initialize LLM analyzer
try:
    llm_analyzer = LLMAnalyzer(provider=Config.LLM_PROVIDER)
    logger.info(f"✅ LLM Analyzer initialized (provider: {Config.LLM_PROVIDER})")
except Exception as e:
    logger.warning(f"⚠️ LLM Analyzer initialization failed: {e}")
    llm_analyzer = None


# =============================================================================
# DATABASE INTEGRATION (Supabase - Ready for implementation)
# =============================================================================

def get_supabase_client():
    """
    Get Supabase client for database operations.
    Uncomment when Supabase credentials are configured.
    """
    # from supabase import create_client
    # client = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)
    # return client
    return None  # Placeholder - using mock data for now


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def calculate_priority_level(avg_travel_time: float) -> str:
    """Calculate priority level based on travel time"""
    if avg_travel_time > 60:
        return "Critical"
    elif avg_travel_time > 45:
        return "High"
    elif avg_travel_time > Config.HSSP_TARGET_TRAVEL_TIME:
        return "Medium"
    else:
        return "Low"


def calculate_accessibility_score(avg_travel_time: float) -> float:
    """
    Calculate accessibility score (0-1) based on travel time.
    Formula: score = 1 - (travel_time / threshold)
    where threshold is 60 minutes (severe inaccessibility)
    """
    threshold = 60  # minutes
    score = max(0, 1 - (avg_travel_time / threshold))
    return round(score, 3)


# =============================================================================
# MOCK DATA FUNCTIONS (Replace with real database queries)
# =============================================================================

def get_accessibility_data_mock():
    """
    Get accessibility analysis data.
    TODO: Replace with real database query from accessibility_metrics table
    """
    return {
        "districts": [
            {"name": "Gasabo", "province": "Kigali", "accessibility_score": 0.89, "avg_travel_time": 18, "coverage": 94, "priority": "Low"},
            {"name": "Gicumbi", "province": "Northern", "accessibility_score": 0.35, "avg_travel_time": 62, "coverage": 58, "priority": "Critical"},
            {"name": "Kayonza", "province": "Eastern", "accessibility_score": 0.52, "avg_travel_time": 45, "coverage": 72, "priority": "High"},
            {"name": "Rusizi", "province": "Western", "accessibility_score": 0.52, "avg_travel_time": 51, "coverage": 68, "priority": "Medium"},
            {"name": "Huye", "province": "Southern", "accessibility_score": 0.72, "avg_travel_time": 38, "coverage": 79, "priority": "Medium"},
        ],
        "stats": {
            "total_facilities": 1247,
            "population_covered": 83,
            "avg_travel_time": 47,
            "underserved_areas": 342,
            "districts_meeting_target": 8,
            "districts_not_meeting_target": 22
        }
    }


def get_predictions_data_mock():
    """Get ML predictions for building classification"""
    return {
        "healthcare_facilities": 156,
        "built_up_areas": 2341,
        "confidence_score": 0.87 if ml_model else 0.0,
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "model_status": "loaded" if ml_model else "not_loaded"
    }


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": ml_model is not None,
        "llm_available": llm_analyzer is not None,
        "version": "2.0"
    })


@app.route('/api/accessibility', methods=['GET'])
def get_accessibility():
    """
    Get accessibility analysis data for all districts.
    Query params:
        - province: Filter by province (optional)
    """
    try:
        province = request.args.get('province')

        # TODO: Replace with real database query
        # supabase = get_supabase_client()
        # query = supabase.table('accessibility_metrics').select('*, geographic_regions(name)')
        # if province:
        #     query = query.eq('geographic_regions.province', province)
        # response = query.execute()

        data = get_accessibility_data_mock()

        # Filter by province if specified
        if province and province != 'all':
            data['districts'] = [d for d in data['districts'] if d['province'].lower() == province.lower()]

        return jsonify(data)

    except Exception as e:
        logger.error(f"Error in /api/accessibility: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    """Get ML predictions summary"""
    try:
        data = get_predictions_data_mock()
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in /api/predictions: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze-region', methods=['POST'])
def analyze_region():
    """Analyze a specific region"""
    try:
        data = request.get_json()
        region_name = data.get('region')

        if not region_name:
            return jsonify({"error": "Region name is required"}), 400

        # TODO: Implement real region analysis with road networks and population data
        # For now, return mock data
        return jsonify({
            "region": region_name,
            "accessibility_score": 0.65,
            "healthcare_facilities": 12,
            "population": 145000,
            "avg_travel_time": 42,
            "recommendation": "Consider 2 new health centers in underserved sectors",
            "priority": "Medium"
        })

    except Exception as e:
        logger.error(f"Error in /api/analyze-region: {e}")
        return jsonify({"error": str(e)}), 400


@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """
    Get AI-generated recommendations.
    Query params:
        - district: Specific district (optional)
    """
    try:
        district = request.args.get('district', 'all')

        # Mock recommendations structure
        # TODO: Generate real recommendations from database + LLM
        recommendations = {
            "immediate_actions": [
                {
                    "action": "Conduct detailed field assessment in Northern Province",
                    "priority": "Critical",
                    "timeline": "1-3 months",
                    "estimated_cost": "$50,000"
                },
                {
                    "action": "Deploy mobile health units to Gicumbi District",
                    "priority": "High",
                    "timeline": "3-6 months",
                    "estimated_cost": "$120,000"
                },
                {
                    "action": "Strengthen referral systems between rural and urban facilities",
                    "priority": "High",
                    "timeline": "6-12 months",
                    "estimated_cost": "$80,000"
                }
            ],
            "strategic_planning": [
                {
                    "initiative": "5-year healthcare infrastructure expansion plan",
                    "description": "Systematic facility placement in underserved districts",
                    "timeframe": "2025-2030",
                    "districts": ["Gicumbi", "Kayonza", "Rusizi"]
                },
                {
                    "initiative": "Telemedicine pilot program",
                    "description": "Virtual consultations for remote areas",
                    "timeframe": "2026-2028",
                    "estimated_reach": "500,000 people"
                },
                {
                    "initiative": "Transportation infrastructure improvements",
                    "description": "Road upgrades connecting rural areas to health facilities",
                    "timeframe": "2025-2029",
                    "impact": "Reduce avg travel time by 15 minutes"
                }
            ],
            "resource_allocation": [
                "Prioritize funding for districts with >45 min travel time",
                "Allocate 60% of budget to Critical and High priority areas",
                "Train and deploy 200 community health workers to underserved sectors",
                "Upgrade existing facility equipment in medium-priority districts"
            ],
            "hssp_alignment": {
                "current_compliance": "37%",
                "target": "100% by 2030",
                "gap": "63%",
                "estimated_completion": "2029"
            }
        }

        return jsonify(recommendations)

    except Exception as e:
        logger.error(f"Error in /api/recommendations: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/llm-insights', methods=['POST'])
def get_llm_insights():
    """
    Get LLM-generated insights and policy recommendations.
    Body: {
        "accessibility_data": {...},
        "underserved_districts": [...]
    }
    """
    try:
        if not llm_analyzer:
            return jsonify({
                "error": "LLM service not available",
                "message": "Please configure OPENAI_API_KEY or HUGGINGFACE_MODEL"
            }), 503

        data = request.get_json()
        accessibility_data = data.get('accessibility_data')
        underserved_districts = data.get('underserved_districts')

        if not accessibility_data or not underserved_districts:
            return jsonify({"error": "Missing required data"}), 400

        # Call LLM analyzer
        logger.info("Calling LLM analyzer for policy insights...")
        result = llm_analyzer.analyze_accessibility(
            accessibility_data,
            underserved_districts
        )

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in /api/llm-insights: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/upload-satellite', methods=['POST'])
def upload_satellite():
    """
    Handle satellite imagery upload and processing.
    Processes GeoTIFF files through ML pipeline.
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']

        if not ml_model:
            return jsonify({
                "error": "ML model not loaded",
                "message": "Run training script to generate model"
            }), 503

        # TODO: Implement real GeoTIFF processing
        # For now, return mock response
        logger.info(f"Processing uploaded file: {file.filename}")

        return jsonify({
            "message": "Image processed successfully",
            "filename": file.filename,
            "predictions": {
                "total_patches_analyzed": 256,
                "buildings_detected": 134,
                "healthcare_facilities": 3,
                "high_confidence_detections": 8,
                "avg_confidence": 0.85
            },
            "note": "Real implementation pending - requires rasterio integration"
        })

    except Exception as e:
        logger.error(f"Error in /api/upload-satellite: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/predict-facility', methods=['POST'])
def predict_facility():
    """
    Predict if an image patch contains a healthcare facility.
    Body: {
        "features": [12 numerical features]
    }
    """
    try:
        if not ml_model:
            return jsonify({
                "error": "ML model not loaded",
                "message": "Train the model first using capstoneNotebook_readable.py"
            }), 503

        data = request.get_json()
        features = data.get('features')

        if not features or len(features) != 12:
            return jsonify({
                "error": "Invalid features",
                "message": "Expected 12 numerical features"
            }), 400

        # Scale features
        features_array = np.array(features).reshape(1, -1)
        features_scaled = ml_scaler.transform(features_array)

        # Predict
        prediction = ml_model.predict(features_scaled)[0]
        probabilities = ml_model.predict_proba(features_scaled)[0]
        confidence = float(max(probabilities))

        return jsonify({
            "is_healthcare_facility": bool(prediction),
            "confidence": confidence,
            "probability_negative": float(probabilities[0]),
            "probability_positive": float(probabilities[1]),
            "model_version": "v1.0"
        })

    except Exception as e:
        logger.error(f"Error in /api/predict-facility: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/model-metrics', methods=['GET'])
def get_model_metrics():
    """
    Get ML model performance metrics.
    Useful for evaluation and monitoring.
    """
    try:
        if not ml_model:
            return jsonify({
                "error": "Model not loaded",
                "status": "not_trained"
            }), 404

        # TODO: Load actual metrics from model training
        # For now, return example metrics
        metrics = {
            "model_info": {
                "name": "Healthcare Facility Classifier",
                "type": "Random Forest",
                "version": "v1.0",
                "training_date": "2025-10-20",
                "n_estimators": 100
            },
            "performance": {
                "accuracy": 0.87,
                "precision": 0.89,
                "recall": 0.79,
                "f1_score": 0.84,
                "rmse": 0.23
            },
            "confusion_matrix": {
                "true_negative": 850,
                "false_positive": 120,
                "false_negative": 85,
                "true_positive": 245
            },
            "feature_importance": {
                "ndvi": 0.23,
                "built_up_index": 0.19,
                "red_mean": 0.15,
                "brightness": 0.12,
                "green_mean": 0.10,
                "blue_mean": 0.08,
                "nir_mean": 0.07,
                "other_features": 0.06
            },
            "training_data": {
                "total_samples": 1300,
                "train_samples": 1040,
                "test_samples": 260,
                "class_balance": "80/20"
            }
        }

        return jsonify(metrics)

    except Exception as e:
        logger.error(f"Error in /api/model-metrics: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/hssp-compliance', methods=['GET'])
def check_hssp_compliance():
    """
    Check compliance with Rwanda HSSP V targets.
    Returns national and district-level compliance metrics.
    """
    try:
        # TODO: Get real data from database
        accessibility_data = get_accessibility_data_mock()

        districts = accessibility_data['districts']
        stats = accessibility_data['stats']

        # Calculate national metrics
        avg_travel_time = stats['avg_travel_time']
        coverage_pct = stats['population_covered']

        # District-level compliance
        district_compliance = []
        for district in districts:
            dist_travel_time = district['avg_travel_time']
            dist_coverage = district['coverage']

            district_compliance.append({
                "district": district['name'],
                "province": district['province'],
                "meets_travel_time_target": dist_travel_time <= Config.HSSP_TARGET_TRAVEL_TIME,
                "meets_coverage_target": dist_coverage >= Config.HSSP_TARGET_COVERAGE,
                "travel_time_gap": max(0, dist_travel_time - Config.HSSP_TARGET_TRAVEL_TIME),
                "coverage_gap": max(0, Config.HSSP_TARGET_COVERAGE - dist_coverage)
            })

        # National compliance
        compliance_report = {
            "national_summary": {
                "travel_time": {
                    "current": avg_travel_time,
                    "target": Config.HSSP_TARGET_TRAVEL_TIME,
                    "gap": max(0, avg_travel_time - Config.HSSP_TARGET_TRAVEL_TIME),
                    "status": "compliant" if avg_travel_time <= Config.HSSP_TARGET_TRAVEL_TIME else "non-compliant",
                    "progress_pct": min(100, (Config.HSSP_TARGET_TRAVEL_TIME / avg_travel_time) * 100)
                },
                "coverage": {
                    "current": coverage_pct,
                    "target": Config.HSSP_TARGET_COVERAGE,
                    "gap": max(0, Config.HSSP_TARGET_COVERAGE - coverage_pct),
                    "status": "compliant" if coverage_pct >= Config.HSSP_TARGET_COVERAGE else "non-compliant",
                    "progress_pct": (coverage_pct / Config.HSSP_TARGET_COVERAGE) * 100
                },
                "districts_compliant": len([d for d in district_compliance if d['meets_travel_time_target']]),
                "districts_total": len(district_compliance),
                "overall_compliance_rate": round(
                    len([d for d in district_compliance if d['meets_travel_time_target'] and d['meets_coverage_target']]) / len(district_compliance) * 100, 1
                )
            },
            "district_compliance": district_compliance,
            "recommendations": [
                f"Focus interventions on {len([d for d in district_compliance if not d['meets_travel_time_target']])} non-compliant districts",
                "Projected full compliance by 2029 with current intervention rate",
                "Consider mobile health units for districts with >60 min travel time"
            ]
        }

        return jsonify(compliance_report)

    except Exception as e:
        logger.error(f"Error in /api/hssp-compliance: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/facilities', methods=['GET'])
def get_facilities():
    """
    Get healthcare facilities data.
    Query params:
        - region_id: Filter by region (optional)
        - facility_type: Filter by type (optional)
    """
    try:
        region_id = request.args.get('region_id')
        facility_type = request.args.get('facility_type')

        # TODO: Query from database
        # supabase = get_supabase_client()
        # query = supabase.table('healthcare_facilities').select('*')
        # if region_id:
        #     query = query.eq('region_id', region_id)
        # if facility_type:
        #     query = query.eq('facility_type', facility_type)
        # response = query.execute()

        # Mock data
        facilities = [
            {
                "id": "1",
                "name": "Kigali University Teaching Hospital (CHUK)",
                "type": "referral_hospital",
                "latitude": -1.9536,
                "longitude": 30.0606,
                "district": "Gasabo",
                "capacity": 500,
                "services": ["emergency", "surgery", "maternity", "ICU"]
            },
            {
                "id": "2",
                "name": "Gicumbi District Hospital",
                "type": "district_hospital",
                "latitude": -1.5761,
                "longitude": 30.0669,
                "district": "Gicumbi",
                "capacity": 150,
                "services": ["general", "maternity", "emergency"]
            }
        ]

        return jsonify({"facilities": facilities, "total": len(facilities)})

    except Exception as e:
        logger.error(f"Error in /api/facilities: {e}")
        return jsonify({"error": str(e)}), 500


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    logger.info("🚀 Starting Healthcare Facility Planning API Server...")
    logger.info(f"   ML Model: {'✅ Loaded' if ml_model else '❌ Not loaded'}")
    logger.info(f"   LLM Service: {'✅ Available' if llm_analyzer else '❌ Not available'}")
    logger.info(f"   HSSP V Targets: {Config.HSSP_TARGET_TRAVEL_TIME} min travel time, {Config.HSSP_TARGET_COVERAGE}% coverage")
    logger.info("   Server running on http://localhost:5000")

    app.run(debug=True, port=5000)
