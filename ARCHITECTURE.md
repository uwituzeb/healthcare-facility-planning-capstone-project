# System Architecture Documentation
## Healthcare Facility Planning - Rwanda

**Last Updated:** 2025-11-03
**Version:** 1.0
**Status:** Development Phase

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [Architecture Layers](#architecture-layers)
4. [Current vs. Proposed State](#current-vs-proposed-state)
5. [Technology Stack](#technology-stack)
6. [Data Flow](#data-flow)
7. [API Endpoints](#api-endpoints)
8. [Database Schema](#database-schema)
9. [Machine Learning Pipeline](#machine-learning-pipeline)
10. [Security & Privacy](#security--privacy)
11. [Deployment Architecture](#deployment-architecture)
12. [Development Roadmap](#development-roadmap)

---

## Executive Summary

This document describes the architecture of the Healthcare Facility Planning system for Rwanda, designed to support data-driven decision-making for equitable healthcare facility placement. The system leverages satellite imagery, machine learning, and large language models to identify underserved areas and generate policy recommendations.

**Key Architectural Goals:**
- **Scalability:** Handle national-level geospatial data
- **Accuracy:** ML-driven facility detection and accessibility analysis
- **Usability:** Intuitive interface for non-technical policymakers
- **Compliance:** Align with Rwanda's HSSP V targets

---

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│         React 19 + Tailwind CSS + Supabase Auth                │
├─────────────────────────────────────────────────────────────────┤
│                      APPLICATION LAYER                          │
│   - Interactive Maps    - Recommendations   - Analytics        │
│   - Admin Dashboard     - Reports           - Data Export       │
└────────────────┬────────────────────────────────────────────────┘
                 │ REST API (JSON)
                 │
┌────────────────┴────────────────────────────────────────────────┐
│                       API GATEWAY (Flask)                       │
│  - Authentication      - Rate Limiting      - CORS             │
│  - Request Validation  - Error Handling     - Logging          │
└────────────┬───────────────────────┬────────────────────────────┘
             │                       │
    ┌────────┴────────┐    ┌────────┴────────────┐
    │   ML SERVICE    │    │   LLM SERVICE       │
    │  - Feature      │    │  - Policy Insights  │
    │    Extraction   │    │  - Recommendations  │
    │  - Predictions  │    │  - Report Gen       │
    └────────┬────────┘    └────────┬────────────┘
             │                       │
    ┌────────┴───────────────────────┴────────────┐
    │           DATA PROCESSING LAYER              │
    │  - Satellite Imagery    - Road Networks     │
    │  - Population Data      - Geospatial Ops    │
    └────────┬─────────────────────────────────────┘
             │
    ┌────────┴────────────────────────────────────┐
    │           DATA STORAGE LAYER                 │
    │  - Supabase (PostgreSQL + PostGIS)          │
    │  - Cloud Storage (Satellite Images)         │
    │  - Model Registry (ML Models)               │
    └──────────────────────────────────────────────┘
```

---

## Architecture Layers

### 1. Presentation Layer (Frontend)

**Technology:** React 19.2.0, Tailwind CSS 3.4.18
**Hosting:** Netlify/Vercel (Proposed)

**Components:**
- **Landing Page** (`landingPage/`) - Public-facing project information
- **Authentication** (`loginPage/`, `SignupPage/`) - User registration and login
- **Dashboard** (`dashboards/`) - Main analytics interface
- **Interactive Map** (`interactiveMap.jsx`) - Geospatial visualization
- **Recommendations** (`recommendations.jsx`) - AI-generated facility placement suggestions
- **Accessibility Analysis** (`accessibilityAnalysis.jsx`) - Healthcare access metrics
- **Reports** (`reports.jsx`) - Report generation and export
- **Admin Panel** (`admin/`) - User approval and system management

**State Management:** React Hooks (useState, useEffect, useContext)
**HTTP Client:** Axios via custom `lib/api.js` wrapper

### 2. API Gateway Layer (Backend)

**Technology:** Flask 2.3.3 (Python)
**Hosting:** Google Cloud Run (Proposed)

**Responsibilities:**
- RESTful API endpoints for frontend consumption
- Request validation and error handling
- Authentication and authorization
- CORS management for cross-origin requests
- Rate limiting and security

**Current Endpoints:**
- `GET /api/health` - Health check
- `GET /api/accessibility` - Accessibility analysis data
- `GET /api/predictions` - ML model predictions
- `POST /api/analyze-region` - Region-specific analysis
- `GET /api/recommendations` - AI-generated recommendations
- `POST /api/upload-satellite` - Satellite imagery upload

**Planned Endpoints:**
- `POST /api/llm-insights` - LLM policy analysis
- `POST /api/predict-facility` - ML facility prediction
- `GET /api/model-metrics` - Model performance metrics
- `GET /api/hssp-compliance` - HSSP V target validation
- `GET /api/facilities` - Healthcare facilities data
- `GET /api/population/:district` - Population data by district

### 3. Machine Learning Layer

**Technology:** Scikit-learn 1.3.0, Rasterio 1.3.8, Patchify 0.2.3
**Model:** Random Forest Classifier

**Pipeline:**
```python
Input: Satellite Image (GeoTIFF)
  ↓
Preprocessing: Load with rasterio
  ↓
Tiling: Extract 256x256 pixel patches (patchify)
  ↓
Feature Extraction: 12 features per patch
  - RGB band statistics (mean, std)
  - NDVI (Normalized Difference Vegetation Index)
  - Built-up index
  - Overall brightness metrics
  ↓
Scaling: StandardScaler normalization
  ↓
Classification: Random Forest (100 estimators)
  ↓
Output: Building/Healthcare Facility Probability
```

**Model Files:**
- `models/healthcare_model.pkl` - Trained Random Forest + Scaler
- `models/metadata.json` - Model version, metrics, training date

### 4. LLM Analysis Layer

**Technology:** Hugging Face Transformers / OpenAI API
**Proposed Models:**
- **Option A:** `microsoft/phi-2` (lightweight, runs locally)
- **Option B:** GPT-3.5-turbo (via OpenAI API)

**Purpose:**
- Analyze accessibility data and generate contextual insights
- Provide policy recommendations aligned with HSSP V
- Synthesize geospatial and demographic data into actionable reports

**Example Workflow:**
```python
Input: Accessibility metrics, underserved districts, population data
  ↓
LLM Prompt Engineering: Structured context with data
  ↓
LLM Inference: Generate recommendations
  ↓
Output: Policy recommendations, priority areas, strategic actions
```

### 5. Data Processing Layer

**Geospatial Processing:**
- **Library:** GeoPandas 0.13.2, Rasterio 1.3.8
- **Operations:** Spatial joins, buffering, intersection, distance calculations
- **Coordinate Systems:** WGS84 (EPSG:4326) for storage, projected CRS for calculations

**Road Network Analysis:**
- **Library:** OSMnx, NetworkX
- **Data Source:** OpenStreetMap
- **Operations:** Shortest path routing, travel time calculation, accessibility scoring

**Population Analysis:**
- **Data Source:** WorldPop (100m resolution raster)
- **Operations:** Population density extraction, cluster identification, demographic analysis

### 6. Data Storage Layer

**Primary Database:** Supabase (PostgreSQL 14 + PostGIS)

**Authentication:** Supabase Auth with Row Level Security (RLS)

**Storage:**
- **Structured Data:** PostgreSQL tables (see Database Schema section)
- **Satellite Images:** Google Cloud Storage / Supabase Storage
- **ML Models:** Versioned storage in Cloud Storage
- **Cached Data:** Redis (optional, for performance)

---

## Current vs. Proposed State

### Current Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| **Frontend UI** | ✅ 90% Complete | Professional, responsive design |
| **User Authentication** | ✅ Complete | Supabase Auth with admin approval |
| **ML Model** | 🟡 Trained but not deployed | Exists in notebook, not in API |
| **LLM Integration** | ❌ Not Implemented | Mock function only |
| **Road Network Analysis** | ❌ Not Implemented | Critical gap |
| **Population Data** | ❌ Mock data only | Hardcoded values |
| **Database Schema** | ⚠️ 8% Complete | Only users table |
| **API Endpoints** | 🟡 Defined but return mock data | Need real data integration |
| **Satellite Processing** | 🟡 Works in notebook | Not integrated with API |
| **Cloud Deployment** | ❌ Not Deployed | Local development only |

### Proposed Final State

| Component | Target | Timeline |
|-----------|--------|----------|
| **Frontend** | ✅ Production-ready | Week 5-6 |
| **Backend API** | ✅ Real data from DB | Week 4 |
| **ML Service** | ✅ Model serving predictions | Week 2 |
| **LLM Service** | ✅ Generating real insights | Week 2 |
| **Road Networks** | ✅ OSM data integrated | Week 3-4 |
| **Population Data** | ✅ WorldPop integrated | Week 3-4 |
| **Database** | ✅ Full schema implemented | Week 3 |
| **Testing** | ✅ >70% coverage | Week 5-6 |
| **Deployment** | ✅ GCP Cloud Run | Week 7-8 |

---

## Technology Stack

### Backend
```yaml
Language: Python 3.9+
Framework: Flask 2.3.3
Extensions:
  - Flask-CORS: Cross-origin resource sharing
  - Flask-SQLAlchemy: ORM (if needed)

Machine Learning:
  - scikit-learn: Random Forest classifier
  - rasterio: GeoTIFF processing
  - geopandas: Geospatial operations
  - patchify: Image tiling

LLM:
  - transformers: Hugging Face models
  - openai: OpenAI API client

Geospatial:
  - geemap: Google Earth Engine integration
  - osmnx: OpenStreetMap road networks
  - networkx: Graph algorithms for routing

Data Processing:
  - numpy: Numerical computing
  - pandas: Data manipulation
  - scipy: Scientific computing
```

### Frontend
```yaml
Language: JavaScript (ES6+)
Framework: React 19.2.0
Routing: React Router DOM 7.9.4
Styling: Tailwind CSS 3.4.18
Icons: Lucide React 0.546.0
HTTP: Axios
Auth: Supabase Client
Build: Create React App
```

### Database
```yaml
Database: PostgreSQL 14 (via Supabase)
Extensions:
  - PostGIS: Geospatial operations
  - pg_cron: Scheduled tasks

Features:
  - Row Level Security (RLS)
  - Real-time subscriptions
  - Edge Functions
  - Storage API
```

### Infrastructure
```yaml
Cloud Provider: Google Cloud Platform
Services:
  - Cloud Run: Backend hosting (serverless containers)
  - Cloud Storage: Satellite imagery, models
  - Cloud Build: CI/CD
  - Secret Manager: Environment variables

Frontend Hosting: Netlify or Vercel
Monitoring: Google Cloud Monitoring + Sentry (error tracking)
```

---

## Data Flow

### 1. User Authentication Flow

```
User → Frontend → Supabase Auth → Database (users table) → RLS Policies
  ↓
Admin Dashboard (approve/reject)
  ↓
User Account Activated
```

### 2. Satellite Image Processing Flow

```
User uploads GeoTIFF
  ↓
Frontend → POST /api/upload-satellite
  ↓
Backend:
  1. Save to Cloud Storage
  2. Load with rasterio
  3. Extract 256x256 patches
  4. Extract 12 features per patch
  5. Scale features
  6. Run ML prediction
  7. Store results in database
  ↓
Return: Detected facilities with coordinates
  ↓
Frontend: Display on interactive map
```

### 3. Accessibility Analysis Flow

```
Request: GET /api/accessibility?district=Gicumbi
  ↓
Backend:
  1. Load district boundary from database
  2. Get healthcare facilities in district
  3. Get population density (WorldPop)
  4. Load road network (OSM)
  5. Calculate travel times:
     - For each population point
     - Find nearest facility
     - Calculate shortest path on road network
     - Compute travel time (distance / avg_speed)
  6. Calculate accessibility score:
     score = 1 - (avg_travel_time / WHO_target)
  7. Store metrics in database
  ↓
Return: {
  district: "Gicumbi",
  accessibility_score: 0.35,
  avg_travel_time: 62 min,
  underserved_population: 180000,
  priority: "Critical"
}
  ↓
Frontend: Display in dashboard
```

### 4. LLM Recommendation Flow

```
Request: GET /api/recommendations?district=Gicumbi
  ↓
Backend:
  1. Fetch accessibility metrics
  2. Fetch population data
  3. Fetch existing facilities
  4. Identify underserved areas
  5. Build LLM prompt:
     "Given accessibility score 0.35, avg travel time 62 min,
      population 485,000, and 12 facilities, recommend
      optimal facility placement aligned with HSSP V."
  6. Call LLM API (OpenAI or Hugging Face)
  7. Parse LLM response
  8. Store in llm_analysis table
  ↓
Return: {
  recommendations: [
    {
      location: "Byumba Sector",
      type: "Health Center",
      priority: "Critical",
      reasoning: {...},
      impact: {...}
    }
  ],
  strategic_actions: [...],
  hssp_alignment: {...}
}
  ↓
Frontend: Display in recommendations component
```

---

## API Endpoints

### Authentication
```http
POST /auth/signup
POST /auth/login
POST /auth/logout
GET /auth/user
```

### Health & Monitoring
```http
GET /api/health
GET /api/version
GET /api/model-metrics
```

### Accessibility Analysis
```http
GET /api/accessibility
GET /api/accessibility/:district
GET /api/hssp-compliance
GET /api/underserved-areas
```

### ML Predictions
```http
POST /api/upload-satellite
POST /api/predict-facility
GET /api/predictions
GET /api/building-clusters
```

### Recommendations & LLM
```http
GET /api/recommendations?district={name}
POST /api/llm-insights
GET /api/reports/:id
POST /api/generate-report
```

### Geospatial Data
```http
GET /api/facilities
GET /api/facilities/:id
GET /api/regions
GET /api/population/:district
GET /api/road-network/:district
```

### Admin
```http
GET /api/admin/users
POST /api/admin/approve-user/:id
POST /api/admin/reject-user/:id
GET /api/admin/analytics
```

---

## Database Schema

### Entity Relationship Diagram

See full ERD in proposal Section 3.5.1. Key tables:

#### Core Tables

**users** (managed by Supabase Auth)
```sql
id: uuid (PK)
email: varchar
created_at: timestamp
metadata: jsonb
```

**geographic_regions**
```sql
id: uuid (PK)
name: varchar(255)
region_type: varchar(50)  -- province, district, sector
parent_id: uuid (FK → geographic_regions)
boundary: geometry(POLYGON, 4326)
created_at: timestamp
```

**healthcare_facilities**
```sql
id: uuid (PK)
name: varchar(255)
facility_type: varchar(50)  -- hospital, clinic, health_center
latitude: decimal(10, 8)
longitude: decimal(11, 8)
region_id: uuid (FK → geographic_regions)
capacity: integer
services: text[]
osm_id: bigint
created_at: timestamp
```

**accessibility_metrics**
```sql
id: uuid (PK)
region_id: uuid (FK → geographic_regions)
accessibility_score: decimal(5, 3)
avg_travel_time_minutes: decimal(6, 2)
population_coverage_pct: decimal(5, 2)
underserved_population: integer
calculation_date: timestamp
```

**population_data**
```sql
id: uuid (PK)
region_id: uuid (FK → geographic_regions)
total_population: integer
density_per_km2: decimal(10, 2)
age_distribution: jsonb
data_year: integer
created_at: timestamp
```

**satellite_images**
```sql
id: uuid (PK)
region_id: uuid (FK → geographic_regions)
image_url: text
acquisition_date: date
resolution_meters: decimal(5, 2)
source: varchar(100)
cloud_cover_pct: decimal(5, 2)
created_at: timestamp
```

**ml_models**
```sql
id: uuid (PK)
model_name: varchar(255)
model_type: varchar(100)
version: varchar(50)
accuracy: decimal(5, 3)
f1_score: decimal(5, 3)
training_date: timestamp
model_file_url: text
created_at: timestamp
```

**llm_analysis**
```sql
id: uuid (PK)
report_id: uuid (FK → analysis_reports)
prompt: text
response: text
model_used: varchar(100)
confidence_score: decimal(5, 3)
created_at: timestamp
```

Full schema SQL migration available in `database/migrations/001_initial_schema.sql`

---

## Machine Learning Pipeline

### Model Training (Offline)

```python
# capstoneNotebook_readable.py

1. Data Collection
   - Satellite imagery: Sentinel-2 via Google Earth Engine
   - Labels: ESA WorldCover + OpenStreetMap facilities

2. Preprocessing
   - Load GeoTIFF images
   - Extract 256x256 pixel patches
   - Balance dataset (handle class imbalance)

3. Feature Engineering
   - RGB statistics (mean, std)
   - NDVI: (NIR - Red) / (NIR + Red)
   - Built-up index
   - Texture features
   Total: 12 features per patch

4. Model Training
   - Algorithm: Random Forest (100 trees)
   - Split: 80% train, 20% test
   - Class weights: balanced
   - Cross-validation: 5-fold

5. Evaluation
   - Accuracy, Precision, Recall, F1
   - Confusion Matrix
   - Feature Importance

6. Model Persistence
   - Save model + scaler as pickle
   - Store in models/healthcare_model.pkl
```

### Model Serving (Online)

```python
# app.py

1. Model Loading
   with open('models/healthcare_model.pkl', 'rb') as f:
       data = pickle.load(f)
       model = data['model']
       scaler = data['scaler']

2. Prediction Endpoint
   POST /api/predict-facility
   Input: {features: [12 values]}
   Output: {
     is_healthcare_facility: bool,
     confidence: float,
     model_version: str
   }

3. Batch Processing
   POST /api/upload-satellite
   - Process entire GeoTIFF
   - Extract all patches
   - Run predictions
   - Return detections
```

---

## Security & Privacy

### Authentication & Authorization
- **Supabase Auth:** OAuth 2.0 compliant
- **Row Level Security (RLS):** Database-level access control
- **JWT Tokens:** Secure session management
- **Role-Based Access Control (RBAC):**
  - `admin`: Full system access
  - `analyst`: Read access, generate reports
  - `viewer`: Read-only access

### Data Privacy
- **Anonymization:** Aggregate population data at sector level
- **No PII:** System does not collect personal health information
- **Secure Storage:** Encrypted at rest (Supabase encryption)
- **HTTPS Only:** Encrypted in transit (TLS 1.3)

### API Security
- **CORS:** Whitelist allowed origins
- **Rate Limiting:** Prevent abuse (e.g., 100 req/min per IP)
- **Input Validation:** Sanitize all user inputs
- **SQL Injection Prevention:** Parameterized queries
- **Error Handling:** Generic error messages (no stack traces in production)

### Compliance
- **GDPR:** User consent, data access requests
- **Rwanda Data Protection Law:** Compliance with national regulations

---

## Deployment Architecture

### Production Environment (GCP)

```
┌─────────────────────────────────────────────┐
│           Cloud Load Balancer               │
│         (HTTPS, SSL Termination)            │
└────────────────┬────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │    Cloud Run Service    │
    │   (Flask API)           │
    │   - Auto-scaling        │
    │   - Serverless          │
    │   - Container-based     │
    └────────┬────────────────┘
             │
    ┌────────┴─────────────────────────┐
    │                                   │
┌───┴────────────┐         ┌───────────┴──────┐
│  Supabase      │         │  Cloud Storage   │
│  (PostgreSQL   │         │  - Satellite     │
│   + PostGIS)   │         │    images        │
│                │         │  - ML models     │
└────────────────┘         └──────────────────┘
```

### Frontend Deployment

```
┌──────────────────────────────┐
│   Netlify / Vercel           │
│   - Static site hosting      │
│   - CDN distribution         │
│   - Automatic HTTPS          │
│   - Git-based deployments    │
└──────────────────────────────┘
```

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml

on: [push]

jobs:
  test:
    - Run pytest (backend)
    - Run Jest (frontend)
    - Code coverage > 70%

  build:
    - Build Docker image
    - Push to Google Container Registry

  deploy:
    - Deploy to Cloud Run (staging)
    - Run integration tests
    - Deploy to Cloud Run (production)
```

---

## Development Roadmap

### Phase 1: Critical Foundation (Weeks 1-2)
- ✅ Train and save ML model
- ✅ Implement LLM integration
- ✅ Set up database schema
- ✅ Create documentation

### Phase 2: Data Integration (Weeks 3-4)
- 🔄 Road network analysis (OSMnx)
- 🔄 Population data integration (WorldPop)
- 🔄 Connect frontend to real API
- 🔄 HSSP V compliance validation

### Phase 3: Production Features (Weeks 5-6)
- 🔄 Satellite image upload processing
- 🔄 Testing infrastructure (pytest, Jest)
- 🔄 Performance optimization
- 🔄 Error handling and logging

### Phase 4: Deployment (Weeks 7-8)
- 🔄 Docker containerization
- 🔄 GCP deployment
- 🔄 CI/CD pipeline
- 🔄 Monitoring and alerts

---

## Appendix

### Key Files Reference

```
project-root/
├── app.py                          # Flask API server
├── capstoneNotebook_readable.py    # ML training pipeline
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── ARCHITECTURE.md                 # This document
├── BACKLOG.md                      # Prioritized task list
├── README.md                       # Project overview
│
├── models/
│   ├── healthcare_model.pkl        # Trained ML model
│   └── metadata.json               # Model info
│
├── database/
│   ├── migrations/
│   │   └── 001_initial_schema.sql  # Database schema
│   └── seed_data.sql               # Initial data
│
├── frontend-react/frontend/
│   ├── src/
│   │   ├── components/             # React components
│   │   ├── lib/
│   │   │   ├── api.js              # API client
│   │   │   └── supabase.js         # Supabase client
│   │   └── App.js                  # Main app
│   └── package.json                # Node dependencies
│
└── data/                           # Data files (not in git)
    ├── rwa_ppp_2020.tif            # Population raster
    └── rwanda_boundary.geojson     # Country boundary
```

### Contact & Support

- **Developer:** Bernice Uwituze
- **Supervisor:** Ndinelao Iitumba
- **Institution:** BSc. Software Engineering Program
- **Repository:** https://github.com/uwituzeb/healthcare-facility-planning-capstone-project

---

**Document Version:** 1.0
**Last Updated:** 2025-11-03
**Next Review:** After Phase 1 completion
