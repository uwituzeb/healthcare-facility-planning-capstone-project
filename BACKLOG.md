# Healthcare Facility Planning - Prioritized Backlog

## 🚨 CRITICAL PRIORITY (Must Complete for Proposal Alignment)

### Issue #1: Implement Real LLM Integration
**Priority:** P0 - Critical
**Effort:** 2-3 days
**Status:** 🔴 Not Started

**Description:**
Replace mock LLM function with actual Hugging Face Transformers integration for generating policy recommendations.

**Proposal Requirement:**
- Section 1.2: "leveraging...LLM to analyze accessibility...generating evidence-based insights"
- Section 3.3.1: "use of a large language model to analyze contextual data"
- Section 3.6: "Hugging Face Transformers for integrating and fine-tuning LLMs"

**Current State:**
- `capstoneNotebook_readable.py:1089` - Mock function returning template strings
- `requirements.txt:18` - `openai==0.27.8` installed but unused

**Implementation Tasks:**
- [ ] Choose LLM: Hugging Face `microsoft/phi-2` (lightweight) OR OpenAI GPT-3.5
- [ ] Create `llm_analysis.py` module
- [ ] Implement `analyze_accessibility_with_llm()` with real API
- [ ] Add `/api/llm-insights` endpoint to app.py
- [ ] Update requirements.txt with `transformers`, `torch`
- [ ] Add environment variable `OPENAI_API_KEY` or use local model
- [ ] Test with real accessibility data
- [ ] Update frontend to display LLM-generated insights

**Files to Modify:**
- `capstoneNotebook_readable.py` (lines 1060-1126)
- `app.py` (add new endpoint)
- `requirements.txt`
- `frontend-react/frontend/src/components/recommendations.jsx`

**Acceptance Criteria:**
- ✅ Real LLM generates contextual recommendations
- ✅ API endpoint returns LLM insights
- ✅ Frontend displays AI-generated policy recommendations
- ✅ Aligned with proposal Section 3.6 tech stack

---

### Issue #2: Train and Deploy ML Model to Production
**Priority:** P0 - Critical
**Effort:** 1-2 days
**Status:** 🔴 Not Started

**Description:**
Train Random Forest model and save to `models/healthcare_model.pkl` so Flask API can serve predictions.

**Proposal Requirement:**
- Section 1.3.1 Objective 2: "Develop a machine learning solution"
- Section 3.3.1: "ML pipeline that classifies building structures"

**Current State:**
- `app.py:12` - Model path points to non-existent file
- Model trained in notebook but not saved
- API returns mock data instead of predictions

**Implementation Tasks:**
- [ ] Create `models/` directory
- [ ] Add model saving function to `capstoneNotebook_readable.py`
- [ ] Train model and save as pickle file
- [ ] Fix `app.py` model loading (lines 14-23)
- [ ] Implement `/api/predict-facility` endpoint
- [ ] Update `/api/upload-satellite` to process real images
- [ ] Add model metrics endpoint `/api/model-metrics`
- [ ] Update .gitignore to handle model files

**Files to Create/Modify:**
- `models/healthcare_model.pkl` (new)
- `capstoneNotebook_readable.py` (add save function)
- `app.py` (fix loading, add prediction endpoint)
- `.gitignore` (add models/ handling)

**Acceptance Criteria:**
- ✅ Model file exists and loads successfully
- ✅ API serves real predictions
- ✅ Satellite image upload processes GeoTIFF files
- ✅ Model metrics exposed via API

---

### Issue #3: Add Road Network Analysis
**Priority:** P0 - Critical
**Effort:** 3-4 days
**Status:** 🔴 Not Started

**Description:**
Implement OSM road network analysis to calculate actual travel times, a core proposal requirement.

**Proposal Requirement:**
- Section 1.2: "proximity to roads" as accessibility factor
- Section 1.3: "based on...road networks"
- Section 1.4 RQ1: "geographic and infrastructural barriers"
- Section 3.3.1: "road networks and proximity to existing facilities"

**Current State:**
- Complete absence of road network analysis
- Travel times are hardcoded mock data
- Cannot calculate actual accessibility scores

**Implementation Tasks:**
- [ ] Install `osmnx` and `networkx` libraries
- [ ] Create `road_network_analysis.py` module
- [ ] Implement `download_road_network()` for Rwanda
- [ ] Implement `calculate_travel_time(origin, destination)` using routing
- [ ] Implement `get_accessibility_score(district)` using road networks
- [ ] Add WHO 25-minute target validation
- [ ] Update `app.py` accessibility endpoint with real calculations
- [ ] Cache road network graph for performance
- [ ] Add road network visualization to frontend map

**Files to Create/Modify:**
- `road_network_analysis.py` (new)
- `app.py` (update `get_accessibility_data()`)
- `requirements.txt` (add osmnx, networkx)
- Database schema (road_networks table)

**Acceptance Criteria:**
- ✅ Download Rwanda road network from OSM
- ✅ Calculate shortest path travel times
- ✅ Accessibility scores based on real road distances
- ✅ Validate against WHO 25-minute target
- ✅ API returns calculated (not mock) travel times

---

### Issue #4: Integrate Population Data
**Priority:** P0 - Critical
**Effort:** 2-3 days
**Status:** 🔴 Not Started

**Description:**
Replace mock population data with real Rwanda census/WorldPop data.

**Proposal Requirement:**
- Section 1.2: "based on...population distribution"
- Section 1.3: "population distribution, existing healthcare facilities"
- Section 1.4 RQ4: "demographic and geographic factors"

**Current State:**
- `app.py:26-43` - Hardcoded mock population values
- No integration with census or demographic data

**Implementation Tasks:**
- [ ] Download WorldPop Rwanda 2020 dataset (100m resolution)
- [ ] Create `data/` directory for population rasters
- [ ] Create `population_analysis.py` module
- [ ] Implement `load_population_data(district)` using rasterio
- [ ] Implement `identify_population_clusters()` for underserved areas
- [ ] Update database schema with population_data table
- [ ] Update `app.py` to use real population data
- [ ] Add population heatmap layer to frontend map

**Files to Create/Modify:**
- `data/rwa_ppp_2020.tif` (new - population raster)
- `population_analysis.py` (new)
- `app.py` (replace mock data)
- Database migration for population_data table

**Acceptance Criteria:**
- ✅ Real population density data loaded
- ✅ Identify high-density population clusters
- ✅ API returns actual population statistics
- ✅ Recommendations based on real demographics

---

### Issue #5: Implement Database Schema
**Priority:** P0 - Critical
**Effort:** 2 days
**Status:** 🔴 Not Started

**Description:**
Implement full database schema from proposal ERD (Section 3.5.1).

**Proposal Requirement:**
- Section 3.5.1: ERD with 12 entities
- Section 3.3.2: "sensitive data...protected through strict access control"

**Current State:**
- Only user authentication implemented (1 of 12 entities)
- No data persistence beyond auth

**Implementation Tasks:**
- [ ] Create Supabase SQL migration file
- [ ] Implement all 12 tables from ERD:
  - geographic_regions
  - healthcare_facilities
  - population_data
  - accessibility_metrics
  - satellite_images
  - building_clusters
  - ml_models
  - analysis_reports
  - road_networks
  - llm_analysis
  - training_data
- [ ] Enable PostGIS extension
- [ ] Add spatial indexes
- [ ] Create Row Level Security (RLS) policies
- [ ] Update app.py to use Supabase client
- [ ] Seed initial data (Rwanda districts)

**Files to Create/Modify:**
- `database/migrations/001_initial_schema.sql` (new)
- `database/seed_data.sql` (new)
- `app.py` (add Supabase integration)
- `.env.example` (add SUPABASE_SERVICE_KEY)

**Acceptance Criteria:**
- ✅ All 12 tables created in Supabase
- ✅ PostGIS enabled for geospatial queries
- ✅ RLS policies enforce security
- ✅ API queries database instead of returning mock data

---

## 🔶 HIGH PRIORITY (Required for Production)

### Issue #6: Frontend API Integration
**Priority:** P1 - High
**Effort:** 2 days
**Status:** 🔴 Not Started

**Description:**
Replace hardcoded frontend data with real API calls.

**Implementation Tasks:**
- [ ] Update `recommendations.jsx` to fetch from `/api/recommendations`
- [ ] Update `accessibilityAnalysis.jsx` to fetch from `/api/accessibility`
- [ ] Update `interactiveMap.jsx` to fetch from `/api/facilities`
- [ ] Add loading states and error handling
- [ ] Implement data refresh functionality
- [ ] Add API error boundaries

**Files to Modify:**
- `recommendations.jsx` (lines 19-89)
- `accessibilityAnalysis.jsx` (lines 61-112)
- `interactiveMap.jsx`
- `dashboardOverview.jsx`

**Acceptance Criteria:**
- ✅ All components fetch real data from API
- ✅ Loading states during data fetch
- ✅ Error handling with user-friendly messages
- ✅ No hardcoded mock data in frontend

---

### Issue #7: Add HSSP V Compliance Validation
**Priority:** P1 - High
**Effort:** 1 day
**Status:** 🔴 Not Started

**Description:**
Implement validation against Rwanda HSSP V targets (WHO 25-minute target).

**Proposal Requirement:**
- Section 1.1: "reduce walking time to under 25 minutes by 2024"
- Section 1.3.1 Objective 3: "alignment with HSSP V targets"

**Implementation Tasks:**
- [ ] Define HSSP V target constants in app.py
- [ ] Create `/api/hssp-compliance` endpoint
- [ ] Calculate compliance metrics per district
- [ ] Add compliance badge to frontend dashboard
- [ ] Generate HSSP V alignment report

**Files to Modify:**
- `app.py` (new endpoint)
- `dashboardOverview.jsx` (add compliance widget)

**Acceptance Criteria:**
- ✅ API reports compliance with 25-minute target
- ✅ District-level compliance tracking
- ✅ Frontend displays compliance status

---

### Issue #8: Implement Real Satellite Image Processing
**Priority:** P1 - High
**Effort:** 2 days
**Status:** 🔴 Not Started

**Description:**
Process uploaded GeoTIFF files through ML pipeline.

**Implementation Tasks:**
- [ ] Update `/api/upload-satellite` endpoint (app.py:116-136)
- [ ] Implement GeoTIFF reading with rasterio
- [ ] Extract patches using patchify
- [ ] Run ML predictions on patches
- [ ] Store results in database
- [ ] Return georeferenced predictions

**Files to Modify:**
- `app.py` (lines 116-136)

**Acceptance Criteria:**
- ✅ Upload GeoTIFF files via API
- ✅ Extract features from satellite imagery
- ✅ Run ML predictions on image patches
- ✅ Return building/facility detections with coordinates

---

## 🟡 MEDIUM PRIORITY (Enhanced Functionality)

### Issue #9: Add Testing Infrastructure
**Priority:** P2 - Medium
**Effort:** 3 days
**Status:** 🔴 Not Started

**Implementation Tasks:**
- [ ] Set up pytest for backend
- [ ] Set up Jest for frontend
- [ ] Write unit tests for ML functions
- [ ] Write API integration tests
- [ ] Write frontend component tests
- [ ] Add GitHub Actions CI/CD
- [ ] Aim for >70% code coverage

**Files to Create:**
- `tests/test_api.py`
- `tests/test_ml_model.py`
- `tests/test_road_network.py`
- `frontend/src/components/__tests__/`
- `.github/workflows/ci.yml`

---

### Issue #10: Deploy to Google Cloud Platform
**Priority:** P2 - Medium
**Effort:** 2 days
**Status:** 🔴 Not Started

**Proposal Requirement:**
- Section 3.6: "Google Cloud Platform (GCP) for scalable computing"

**Implementation Tasks:**
- [ ] Create Dockerfile for Flask app
- [ ] Build Docker image
- [ ] Deploy to GCP Cloud Run
- [ ] Set up Cloud Storage for satellite images
- [ ] Configure environment variables
- [ ] Set up custom domain
- [ ] Deploy frontend to Netlify/Vercel

**Files to Create:**
- `Dockerfile`
- `docker-compose.yml`
- `.gcloudignore`
- `cloudbuild.yaml`

---

### Issue #11: Add Model Performance Metrics Dashboard
**Priority:** P2 - Medium
**Effort:** 1 day
**Status:** 🔴 Not Started

**Proposal Requirement:**
- Section 1.3.1 Objective 3: "Evaluation...using measurable metrics"

**Implementation Tasks:**
- [ ] Create `/api/model-metrics` endpoint
- [ ] Expose accuracy, F1, precision, recall
- [ ] Create metrics visualization component
- [ ] Add confusion matrix display
- [ ] Track model performance over time

---

## 🟢 LOW PRIORITY (Nice to Have)

### Issue #12: Optimize for Large Datasets
**Priority:** P3 - Low
**Effort:** 3 days
**Status:** 🔴 Not Started

**Implementation Tasks:**
- [ ] Implement batch processing for satellite images
- [ ] Add Redis caching for frequently accessed data
- [ ] Optimize database queries with proper indexes
- [ ] Add pagination to API endpoints
- [ ] Implement lazy loading in frontend

---

### Issue #13: Add Export Functionality
**Priority:** P3 - Low
**Effort:** 1 day
**Status:** 🔴 Not Started

**Implementation Tasks:**
- [ ] Implement PDF report generation
- [ ] Implement Excel export for data tables
- [ ] Implement GeoJSON export for map data
- [ ] Add "Export Report" button functionality

---

## 📊 BACKLOG SUMMARY

| Priority | Count | Total Effort |
|----------|-------|--------------|
| P0 - Critical | 5 issues | 12-17 days |
| P1 - High | 3 issues | 5 days |
| P2 - Medium | 3 issues | 6 days |
| P3 - Low | 2 issues | 4 days |
| **TOTAL** | **13 issues** | **27-32 days** |

## 🎯 SPRINT PLANNING

### Sprint 1 (Week 1-2): Critical Foundation
- Issue #2: ML Model Deployment
- Issue #1: LLM Integration
- Issue #5: Database Schema

### Sprint 2 (Week 3-4): Data Integration
- Issue #3: Road Network Analysis
- Issue #4: Population Data
- Issue #6: Frontend API Integration

### Sprint 3 (Week 5-6): Production Features
- Issue #7: HSSP V Compliance
- Issue #8: Satellite Image Processing
- Issue #9: Testing Infrastructure

### Sprint 4 (Week 7-8): Deployment & Polish
- Issue #10: GCP Deployment
- Issue #11: Metrics Dashboard
- Documentation updates
