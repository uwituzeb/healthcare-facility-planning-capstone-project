"""
Healthcare Facility Placement Model - Backend API
Serves model outputs to React frontend dashboards
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load model outputs
DATA_DIR = '/'

class HealthcareDataService:
    """Service to load and serve healthcare model data"""
    
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        """Load all model outputs"""
        try:
            # Load comprehensive analysis
            self.districts_df = pd.read_csv(f'{DATA_DIR}/comprehensive_healthcare_access_analysis.csv')
            
            # Load recommendations
            self.recommendations_df = pd.read_csv(f'{DATA_DIR}/facility_placement_recommendations.csv')
            
            # Load API output
            with open(f'{DATA_DIR}/api_output.json', 'r') as f:
                self.api_data = json.load(f)
            
            print("✓ Data loaded successfully")
        except Exception as e:
            print(f"Warning: Could not load data files: {e}")
            self.districts_df = pd.DataFrame()
            self.recommendations_df = pd.DataFrame()
            self.api_data = {}
    
    def get_dashboard_stats(self):
        """Get overview statistics for dashboard"""
        if self.api_data:
            return self.api_data.get('dashboard_stats', {})
        
        # Fallback calculation if API output not available
        return {
            'total_facilities': len(self.districts_df) * 15,  # Estimate
            'population_covered_pct': round(float(self.districts_df['composite_access_score'].mean()), 1),
            'avg_travel_time_min': round(float(self.districts_df['travel_time_min'].mean()), 1),
            'underserved_districts': int((self.districts_df['priority_level'].isin(['Critical', 'High'])).sum()),
            'national_access_score': round(float(self.districts_df['composite_access_score'].mean()), 1),
            'cbhi_coverage_pct': round(float(self.districts_df['cbhi_coverage_pct'].mean()), 1),
            'total_population': int(self.districts_df['population'].sum())
        }
    
    def get_districts_data(self, province=None):
        """Get district-level data with optional province filter"""
        df = self.districts_df.copy()
        
        if province and province.lower() != 'all':
            df = df[df['province'].str.lower() == province.lower()]
        
        districts = []
        for idx, row in df.iterrows():
            districts.append({
                'id': int(idx),
                'name': str(row['district']),
                'province': str(row['province']),
                'population': int(row['population']),
                'latitude': float(row['latitude']),
                'longitude': float(row['longitude']),
                'composite_access_score': round(float(row['composite_access_score']), 1),
                'priority': str(row['priority_level']),
                'geographic_score': round(float(row['geographic_accessibility_score']), 1),
                'availability_score': round(float(row['availability_score']), 1),
                'affordability_score': round(float(row['affordability_score']), 1),
                'acceptability_score': round(float(row['acceptability_score']), 1),
                'accommodation_score': round(float(row['accommodation_score']), 1),
                'travel_time_min': round(float(row['travel_time_min']), 1),
                'distance_km': round(float(row['distance_km']), 1),
                'nearest_facility': str(row['nearest_facility']),
                'cbhi_coverage': round(float(row['cbhi_coverage_pct']), 1),
                'need_index': round(float(row['need_index']), 2),
                'facility_density_per_10k': round(float(row['facility_density_per_10k']), 2),
                'doctors_per_10k': round(float(row['doctors_per_10k']), 2),
                'nurses_per_10k': round(float(row['nurses_per_10k']), 2),
                'beds_per_10k': round(float(row['beds_per_10k']), 2)
            })
        
        return districts
    
    def get_recommendations(self, n=10):
        """Get top N facility placement recommendations"""
        df = self.recommendations_df.head(n)
        
        recommendations = []
        for idx, row in df.iterrows():
            recommendations.append({
                'id': int(row['rank']),
                'priority': str(row['priority_level']),
                'location': str(row['district']),
                'province': str(row['province']),
                'coordinates': {
                    'lat': float(row['latitude']),
                    'lng': float(row['longitude'])
                },
                'type': str(row['recommended_facility_type']),
                'reasoning': {
                    'population': f"{int(row['population']):,} residents in district",
                    'distance': f"Average {row['expected_travel_reduction_min']} min travel reduction",
                    'demographics': f"{int(row['impact_population']):,} people will be served",
                    'infrastructure': str(row['primary_bottlenecks'])
                },
                'impact': {
                    'populationServed': f"{int(row['impact_population']):,}+",
                    'travelTimeReduction': f"{row['expected_travel_reduction_min']:.0f} minutes",
                    'coverageIncrease': f"{row['expected_coverage_increase_pct']:.1f}%",
                    'estimatedCost': f"${int(row['estimated_cost_usd']):,}"
                },
                'aiInsight': f"District shows composite access score of {row['current_access_score']:.1f}/100. Primary bottlenecks: {row['primary_bottlenecks']}. Expected to serve {int(row['impact_population']):,} people with {row['expected_coverage_increase_pct']:.1f}% coverage increase.",
                'confidence': int(row['confidence_score']),
                'status': 'recommended' if row['implementation_timeline'] == 'Immediate' else 'under-review',
                'implementation_timeline': str(row['implementation_timeline'])
            })
        
        return recommendations
    
    def get_province_summary(self):
        """Get province-level summary"""
        summary = self.districts_df.groupby('province').agg({
            'population': 'sum',
            'composite_access_score': 'mean',
            'priority_level': lambda x: (x.isin(['Critical', 'High'])).sum()
        }).reset_index()
        
        provinces = []
        for idx, row in summary.iterrows():
            provinces.append({
                'name': str(row['province']),
                'total_population': int(row['population']),
                'avg_access_score': round(float(row['composite_access_score']), 1),
                'high_priority_districts': int(row['priority_level'])
            })
        
        return provinces
    
    def get_underserved_areas(self, limit=10):
        """Get most underserved areas"""
        df = self.districts_df.nlargest(limit, 'need_index')
        
        areas = []
        for idx, row in df.iterrows():
            areas.append({
                'area': f"{row['district']} District",
                'population': f"{int(row['population']):,}",
                'nearestFacility': f"{row['distance_km']:.1f} km",
                'travelTime': f"{row['travel_time_min']:.0f} min",
                'severity': str(row['priority_level']),
                'recommendation': self._get_recommendation_text(row)
            })
        
        return areas
    
    def _get_recommendation_text(self, row):
        """Generate recommendation text based on scores"""
        if row['composite_access_score'] < 45:
            return "Urgent: Multiple new facilities required"
        elif row['composite_access_score'] < 60:
            return "Priority: New health center needed"
        else:
            return "Consider: Mobile health services or clinic upgrade"
    
    def get_accessibility_analysis(self, province=None):
        """Get comprehensive accessibility analysis"""
        df = self.districts_df.copy()
        
        if province and province.lower() != 'all':
            df = df[df['province'].str.lower() == province.lower()]
        
        return {
            'key_metrics': {
                'avg_travel_time': round(float(df['travel_time_min'].mean()), 1),
                'population_coverage': round(float((df['composite_access_score'] >= 60).sum() / len(df) * 100), 1),
                'facility_density': round(float(df['facility_density_per_10k'].mean()), 2),
                'meeting_who_standards': round(float((df['availability_score'] >= 60).sum() / len(df) * 100), 1)
            },
            'district_analysis': self.get_districts_data(province),
            'underserved_areas': self.get_underserved_areas(),
            'trends': {
                'travel_time_change': -3,  # Mock improvement
                'coverage_change': 5,
                'facility_density_change': 0.4,
                'who_standards_change': 8
            }
        }

# Initialize data service
data_service = HealthcareDataService()

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0'
    })

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard overview statistics"""
    try:
        stats = data_service.get_dashboard_stats()
        return jsonify({
            'success': True,
            'data': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/districts', methods=['GET'])
def get_districts():
    """Get all districts data with optional province filter"""
    try:
        province = request.args.get('province', 'all')
        districts = data_service.get_districts_data(province)
        
        return jsonify({
            'success': True,
            'data': districts,
            'count': len(districts),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/districts/<string:district_name>', methods=['GET'])
def get_district_detail(district_name):
    """Get detailed information for a specific district"""
    try:
        districts = data_service.get_districts_data()
        district = next((d for d in districts if d['name'].lower() == district_name.lower()), None)
        
        if not district:
            return jsonify({
                'success': False,
                'error': 'District not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': district,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get facility placement recommendations"""
    try:
        limit = int(request.args.get('limit', 10))
        recommendations = data_service.get_recommendations(limit)
        
        return jsonify({
            'success': True,
            'data': recommendations,
            'count': len(recommendations),
            'total_investment': sum([int(r['impact']['estimatedCost'].replace('$', '').replace(',', '')) for r in recommendations]),
            'total_impact_population': sum([int(r['impact']['populationServed'].replace('+', '').replace(',', '')) for r in recommendations]),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/provinces', methods=['GET'])
def get_provinces():
    """Get province-level summary"""
    try:
        provinces = data_service.get_province_summary()
        
        return jsonify({
            'success': True,
            'data': provinces,
            'count': len(provinces),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/accessibility', methods=['GET'])
def get_accessibility():
    """Get comprehensive accessibility analysis"""
    try:
        province = request.args.get('province', 'all')
        analysis = data_service.get_accessibility_analysis(province)
        
        return jsonify({
            'success': True,
            'data': analysis,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/underserved', methods=['GET'])
def get_underserved():
    """Get underserved areas"""
    try:
        limit = int(request.args.get('limit', 10))
        areas = data_service.get_underserved_areas(limit)
        
        return jsonify({
            'success': True,
            'data': areas,
            'count': len(areas),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/priorities', methods=['GET'])
def get_priorities():
    """Get priority areas for intervention"""
    try:
        # Get high priority districts
        districts = data_service.get_districts_data()
        high_priority = [d for d in districts if d['priority'] in ['Critical', 'High']]
        high_priority.sort(key=lambda x: x['need_index'], reverse=True)
        
        priorities = []
        for d in high_priority[:10]:
            priorities.append({
                'area': f"{d['name']} District",
                'population': f"{d['population']:,}",
                'facilities': str(int(d['facility_density_per_10k'] * d['population'] / 10000)),
                'priority': d['priority'],
                'recommendation': f"Accessibility score: {d['composite_access_score']}/100. {'Multiple facilities needed' if d['composite_access_score'] < 50 else 'One facility recommended'}"
            })
        
        return jsonify({
            'success': True,
            'data': priorities,
            'count': len(priorities),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hssp-targets', methods=['GET'])
def get_hssp_targets():
    """Get HSSP V targets progress"""
    try:
        stats = data_service.get_dashboard_stats()
        
        targets = {
            'universal_coverage': stats.get('population_covered_pct', 83),
            'travel_time_25min': round((data_service.districts_df['travel_time_min'] <= 25).sum() / len(data_service.districts_df) * 100, 1),
            'facility_modernization': 45,  # Mock data
            'rural_coverage': round((data_service.districts_df[data_service.districts_df['urban_rural'] == 'Rural']['composite_access_score'] >= 60).sum() / len(data_service.districts_df[data_service.districts_df['urban_rural'] == 'Rural']) * 100, 1)
        }
        
        return jsonify({
            'success': True,
            'data': targets,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analysis/recent', methods=['GET'])
def get_recent_analysis():
    """Get recent analysis records"""
    try:
        # Mock recent analysis data
        analyses = [
            {
                'region': 'Kigali - Gasabo District',
                'status': 'Completed',
                'date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
                'coverage': '89%'
            },
            {
                'region': 'Eastern Province - Rwamagana',
                'status': 'In Progress',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'coverage': '67%'
            },
            {
                'region': 'Southern Province - Huye',
                'status': 'Pending',
                'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'coverage': '72%'
            }
        ]
        
        return jsonify({
            'success': True,
            'data': analyses,
            'count': len(analyses),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export', methods=['GET'])
def export_data():
    """Export comprehensive data"""
    try:
        format_type = request.args.get('format', 'json')
        
        if format_type == 'csv':
            # Return path to CSV file
            return jsonify({
                'success': True,
                'file_path': f'{DATA_DIR}/comprehensive_healthcare_access_analysis.csv',
                'file_name': 'healthcare_access_analysis.csv'
            })
        else:
            # Return JSON data
            return jsonify({
                'success': True,
                'data': data_service.api_data,
                'timestamp': datetime.now().isoformat()
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/facilities', methods=['GET'])
def get_facilities():
    """Get all healthcare facilities"""
    try:
        if 'facilities' in data_service.api_data:
            facilities = data_service.api_data['facilities']
        else:
            # Generate sample facilities from district data
            facilities = []
            for idx, row in data_service.districts_df.iterrows():
                facilities.append({
                    'id': int(idx),
                    'name': row['nearest_facility'],
                    'type': row['nearest_facility_type'],
                    'latitude': float(row['latitude']),
                    'longitude': float(row['longitude']),
                    'district': row['district'],
                    'beds': int(row['beds_per_10k'] * row['population'] / 10000) if 'beds_per_10k' in row else None,
                    'emergency': 'yes' if 'Hospital' in str(row['nearest_facility_type']) else 'no'
                })
        
        return jsonify({
            'success': True,
            'data': facilities,
            'count': len(facilities),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("\nStarting server on http://localhost:5000")

    
    app.run(debug=True, host='0.0.0.0', port=5000)