from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare_planning.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Analysis results model
class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    analysis_type = db.Column(db.String(50), nullable=False)
    results = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('signup.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('signup.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Load analysis results for the user
    results = AnalysisResult.query.filter_by(user_id=session['user_id']).order_by(AnalysisResult.created_at.desc()).all()
    
    return render_template('dashboard.html', results=results)

@app.route('/api/accessibility-analysis', methods=['POST'])
def accessibility_analysis():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # This would integrate with your ML model
        # For now, return sample data
        sample_results = {
            'underserved_districts': [
                {'name': 'Nyagatare', 'score': 0.23, 'priority': 'High'},
                {'name': 'Gatsibo', 'score': 0.31, 'priority': 'High'},
                {'name': 'Kayonza', 'score': 0.35, 'priority': 'Medium'}
            ],
            'recommendations': [
                'Establish new health centers in Nyagatare district',
                'Improve road infrastructure in Gatsibo',
                'Consider mobile health units for remote areas'
            ],
            'analysis_date': datetime.utcnow().isoformat()
        }
        
        # Save results to database
        result = AnalysisResult(
            user_id=session['user_id'],
            analysis_type='accessibility',
            results=json.dumps(sample_results)
        )
        db.session.add(result)
        db.session.commit()
        
        return jsonify(sample_results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/facility-recommendations', methods=['POST'])
def facility_recommendations():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        district = data.get('district')
        
        # This would integrate with your ML model for facility placement
        recommendations = {
            'district': district,
            'recommended_locations': [
                {'lat': -1.9441, 'lon': 30.0619, 'type': 'Health Center', 'priority': 'High'},
                {'lat': -1.9500, 'lon': 30.0700, 'type': 'Clinic', 'priority': 'Medium'}
            ],
            'reasoning': f'Based on population density and accessibility analysis for {district}',
            'estimated_impact': 'Could serve 15,000+ people within 5km radius'
        }
        
        return jsonify(recommendations)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
