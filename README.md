# Healthcare Facility Planning Capstone Project
## Enhancing Health Equity: A Data-Driven Approach for Health Facility Placement in Rwanda

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Overview

This project develops an **ML-driven web application** to guide policymakers in **healthcare facility planning and placement** in Rwanda. The system leverages:

- 🛰️ **Satellite Imagery Analysis** (Sentinel-2 via Google Earth Engine)
- 🤖 **Machine Learning** (Random Forest for facility detection)
- 💡 **Large Language Models** (AI-powered policy recommendations)
- 🗺️ **Geospatial Analysis** (OSM road networks, population density)
- 📊 **Interactive Dashboards** (React-based policymaker interface)

**Mission:** Support Rwanda's path to Universal Health Coverage (UHC) by 2030 by identifying underserved areas and optimizing facility placement aligned with the **Health Sector Strategic Plan V (HSSP V)** targets.

---

## 🎯 Key Features

### ✅ Implemented
- **Professional React UI** with interactive maps, dashboards, and analytics
- **User Authentication** via Supabase with admin approval workflow
- **ML Model** (Random Forest) for built-up area classification from satellite imagery
- **LLM Integration** for AI-generated policy insights and recommendations
- **REST API** with Flask backend (10+ endpoints)
- **HSSP V Compliance Tracking** (WHO 25-minute target validation)
- **Database Schema** (PostgreSQL + PostGIS ready)

### 🚧 In Progress
- Real-time satellite image processing via API
- Road network analysis (OSMnx integration)
- Population data integration (WorldPop)
- Frontend-backend data flow connection
- Testing infrastructure
- Cloud deployment (GCP)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────┐
│    React Frontend (Tailwind CSS)       │
│    - Interactive Maps                   │
│    - Recommendations Dashboard          │
│    - Accessibility Analysis             │
└──────────────┬──────────────────────────┘
               │ REST API
┌──────────────┴──────────────────────────┐
│    Flask Backend API                    │
│    - ML Predictions                     │
│    - LLM Insights                       │
│    - HSSP V Compliance                  │
└──────────────┬──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│    Data Layer                           │
│    - Supabase (PostgreSQL + PostGIS)   │
│    - Google Earth Engine               │
│    - OpenStreetMap                      │
└─────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+ and npm
- Git
- (Optional) Google Earth Engine account
- (Optional) OpenAI API key for LLM features

### 1. Clone Repository

```bash
git clone https://github.com/uwituzeb/healthcare-facility-planning-capstone-project.git
cd healthcare-facility-planning-capstone-project
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables template
cp .env.example .env
# Edit .env and add your API keys (OpenAI, Supabase, etc.)

# Run Flask API
python app_enhanced.py
```

Backend will run on `http://localhost:5000`

### 3. Frontend Setup

```bash
cd frontend-react/frontend

# Install dependencies
npm install

# Set environment variables
# Create .env.local with:
# REACT_APP_API_URL=http://localhost:5000
# REACT_APP_SUPABASE_URL=your-supabase-url
# REACT_APP_SUPABASE_ANON_KEY=your-supabase-key

# Run development server
npm start
```

Frontend will run on `http://localhost:3000`

### 4. Train ML Model (First Time Only)

```bash
# Ensure virtual environment is activated
python capstoneNotebook_readable.py

# This will:
# - Download satellite imagery
# - Extract features
# - Train Random Forest model
# - Save to models/healthcare_model.pkl
```

---

## 📂 Project Structure

```
healthcare-facility-planning-capstone-project/
├── app.py                          # Original Flask API
├── app_enhanced.py                 # ✨ Enhanced API with LLM & ML integration
├── llm_analysis.py                 # ✨ LLM integration module (NEW)
├── capstoneNotebook_readable.py    # ML training pipeline
├── capstoneNotebook.ipynb          # Jupyter notebook version
├── requirements.txt                # Python dependencies (UPDATED)
│
├── models/                         # ✨ ML models (NEW)
│   ├── healthcare_model.pkl        # Trained Random Forest + Scaler
│   └── README.md                   # Model documentation
│
├── database/                       # ✨ Database schema (NEW)
│   └── migrations/
│       └── 001_initial_schema.sql  # Full PostgreSQL + PostGIS schema
│
├── frontend-react/frontend/        # React application
│   ├── src/
│   │   ├── components/             # UI components
│   │   │   ├── recommendations.jsx
│   │   │   ├── accessibilityAnalysis.jsx
│   │   │   ├── interactiveMap.jsx
│   │   │   └── dashboards/
│   │   ├── lib/
│   │   │   ├── api.js              # API client
│   │   │   └── supabase.js         # Supabase client
│   │   └── App.js
│   └── package.json
│
├── data/                           # Data files (not tracked in git)
├── logs/                           # Application logs
│
├── .env.example                    # ✨ Environment variables template (NEW)
├── ARCHITECTURE.md                 # ✨ System architecture docs (NEW)
├── BACKLOG.md                      # ✨ Prioritized task backlog (NEW)
└── README.md                       # This file (UPDATED)
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_SECRET_KEY=your-secret-key

# Supabase (Database & Auth)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# LLM Configuration (Choose one)
# Option 1: OpenAI
OPENAI_API_KEY=sk-your-openai-key
LLM_PROVIDER=openai

# Option 2: Hugging Face
# LLM_PROVIDER=huggingface
# HUGGINGFACE_API_KEY=hf_your-token

# HSSP V Targets
HSSP_TARGET_TRAVEL_TIME=25  # WHO target (minutes)
HSSP_TARGET_COVERAGE=95     # percentage
```

See [.env.example](.env.example) for full configuration options.

---

## 📡 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check & system status |
| `GET` | `/api/accessibility` | Accessibility metrics by district |
| `GET` | `/api/predictions` | ML model predictions summary |
| `POST` | `/api/analyze-region` | Analyze specific region |
| `GET` | `/api/recommendations` | AI-generated recommendations |

### New Enhanced Endpoints ✨

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/llm-insights` | **LLM-powered policy insights** |
| `POST` | `/api/predict-facility` | **ML facility prediction** |
| `GET` | `/api/model-metrics` | **Model performance metrics** |
| `GET` | `/api/hssp-compliance` | **HSSP V target validation** |
| `POST` | `/api/upload-satellite` | Process satellite imagery |
| `GET` | `/api/facilities` | Healthcare facilities data |

Full API documentation: See [ARCHITECTURE.md](ARCHITECTURE.md#api-endpoints)

---

## 🤖 Machine Learning Pipeline

### Model: Random Forest Classifier

**Input:** 256x256 pixel satellite image patch
**Features (12):**
- RGB band statistics (mean, std)
- NDVI (Normalized Difference Vegetation Index)
- Built-up index
- Brightness metrics

**Output:** Binary classification (Healthcare facility: Yes/No)

### Training

```bash
python capstoneNotebook_readable.py
```

### Usage

```python
import pickle
import numpy as np

# Load model
with open('models/healthcare_model.pkl', 'rb') as f:
    data = pickle.load(f)
    model = data['model']
    scaler = data['scaler']

# Predict
features = [...]  # 12 features from image patch
features_scaled = scaler.transform([features])
prediction = model.predict(features_scaled)[0]
confidence = model.predict_proba(features_scaled)[0]

print(f"Healthcare facility detected: {bool(prediction)}")
print(f"Confidence: {max(confidence):.2%}")
```

---

## 💡 LLM Integration

The system uses Large Language Models to generate contextual policy recommendations:

### Supported Providers

1. **OpenAI GPT-3.5/GPT-4** (Recommended)
2. **Hugging Face Models** (e.g., microsoft/phi-2)

### Usage Example

```python
from llm_analysis import analyze_with_llm

result = analyze_with_llm(
    accessibility_data={
        'total_districts': 30,
        'underserved_count': 12,
        'average_accessibility': 0.58,
        'avg_travel_time': 47
    },
    underserved_districts=[
        {'district': 'Gicumbi', 'accessibility_score': 0.35, ...},
        ...
    ]
)

print(result['insights'])
print(result['immediate_recommendations'])
print(result['hssp_alignment'])
```

See [llm_analysis.py](llm_analysis.py) for full documentation.

---

## 🗄️ Database Schema

The system uses **PostgreSQL with PostGIS** extension (via Supabase):

### Key Tables

- `geographic_regions` - Administrative boundaries
- `healthcare_facilities` - Facilities with locations
- `accessibility_metrics` - Calculated accessibility scores
- `population_data` - Demographic information
- `satellite_images` - Imagery repository
- `ml_models` - Model registry with metrics
- `llm_analysis` - AI-generated insights

### Setup

```bash
# 1. Create Supabase project at https://supabase.com

# 2. Run migration in Supabase SQL Editor
cat database/migrations/001_initial_schema.sql
# Copy and execute in Supabase

# 3. Update .env with Supabase credentials
```

Full schema: [database/migrations/001_initial_schema.sql](database/migrations/001_initial_schema.sql)

---

## 🎯 HSSP V Compliance

The system validates against Rwanda's **Health Sector Strategic Plan V** targets:

- ✅ **25-minute maximum travel time** (WHO target)
- ✅ **95% population coverage**
- ✅ **5 facilities per 10,000 people**

### Check Compliance

```bash
curl http://localhost:5000/api/hssp-compliance
```

Returns national and district-level compliance metrics.

---

## 📊 Data Sources

1. **Satellite Imagery:** Sentinel-2 (Google Earth Engine)
2. **Land Cover:** ESA WorldCover 2021
3. **Healthcare Facilities:** OpenStreetMap
4. **Population Data:** WorldPop (100m resolution)
5. **Road Networks:** OpenStreetMap (via OSMnx)

---

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-flask

# Run tests
pytest tests/ --cov=app --cov-report=html

# Frontend tests
cd frontend-react/frontend
npm test
```

---

## 🚀 Deployment

### Docker (Recommended)

```bash
# Build image
docker build -t healthcare-api .

# Run container
docker run -p 5000:5000 --env-file .env healthcare-api
```

### Google Cloud Platform

```bash
# Deploy to Cloud Run
gcloud builds submit --tag gcr.io/PROJECT_ID/healthcare-api
gcloud run deploy --image gcr.io/PROJECT_ID/healthcare-api --platform managed
```

See [ARCHITECTURE.md](ARCHITECTURE.md#deployment-architecture) for details.

---

## 📚 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture & design
- [BACKLOG.md](BACKLOG.md) - Prioritized development tasks
- [.env.example](.env.example) - Environment configuration
- [models/README.md](models/README.md) - ML model documentation

---

## 🛠️ Development Roadmap

See [BACKLOG.md](BACKLOG.md) for the full prioritized backlog.

### Phase 1: Critical Foundation (Weeks 1-2) ✅
- [x] LLM integration module
- [x] Database schema design
- [x] Enhanced API with ML integration
- [x] Documentation

### Phase 2: Data Integration (Weeks 3-4) 🔄
- [ ] Road network analysis (OSMnx)
- [ ] Population data integration
- [ ] Frontend-backend connection
- [ ] HSSP V validation

### Phase 3: Production (Weeks 5-6)
- [ ] Testing infrastructure
- [ ] Performance optimization
- [ ] Error handling & logging

### Phase 4: Deployment (Weeks 7-8)
- [ ] Docker containerization
- [ ] GCP deployment
- [ ] CI/CD pipeline

---

## 🔗 Useful Links

- [Research Proposal](https://docs.google.com/document/d/1oD9Z0VMz-l0DHpFxPu1oSyIhshzPu5Mk/edit)
- [Initial Demo](https://drive.google.com/drive/folders/1QuFkSdhaahjhSNORI3h6Uj6ww63RIv6k)
- [Google Colab](https://colab.research.google.com/drive/14DFmzp2NZUoD-YDjNYutxfCC8dWomqqi)
- [Figma Design](https://www.figma.com/design/vpXG6EV3bQxsLMF8JYRGjV/capstone)
- [GitHub Repository](https://github.com/uwituzeb/healthcare-facility-planning-capstone-project)

---

## 👥 Team

- **Developer:** Bernice Uwituze
- **Supervisor:** Ndinelao Iitumba
- **Institution:** BSc. Software Engineering Program

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Rwanda Ministry of Health (HSSP V framework)
- Google Earth Engine (satellite imagery)
- OpenStreetMap contributors (geospatial data)
- Supabase (database & authentication)

---

## 📧 Contact & Support

For questions or issues:
1. Open a [GitHub Issue](https://github.com/uwituzeb/healthcare-facility-planning-capstone-project/issues)
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
3. Check [BACKLOG.md](BACKLOG.md) for known issues

---

**Made with ❤️ for advancing healthcare equity in Rwanda**
