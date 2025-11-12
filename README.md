# HealthAccess

## Overview

ML-powered healthcare facility planning system for Rwanda using satellite imagery and machine learning to support Rwanda's path to Universal Health Coverage (UHC) by 2030 by identifying underserved areas and optimizing facility placement aligned with the Health Sector Strategic Plan V (HSSP V) targets. The web application aims to help policymakers and healthcare professionals identify optimal locations for new healthcare facilities by combining:

- **Satellite Imagery Analysis** (Sentinel-2) - Identifies built-up areas suitable for facilities
- **Machine Learning** (Random Forest) - Predicts facility suitability with 98.9% accuracy
- **Geospatial Analysis** (PostGIS) - Analyzes accessibility and travel times
- **Interactive Mapping** (Mapbox) - Visualizes recommendations and current facilities

## Useful Links

- [Initial Project Demo](https://drive.google.com/drive/folders/1QuFkSdhaahjhSNORI3h6Uj6ww63RIv6k?usp=sharing)
- [Final Project Demo](https://drive.google.com/drive/folders/1InSGp7JT0DwwQj24zwR-4GJ39t2t0rxv?usp=drive_link)
- [Initial Google Colab](https://colab.research.google.com/drive/14DFmzp2NZUoD-YDjNYutxfCC8dWomqqi?usp=sharing)
- [Research Proposal](https://docs.google.com/document/d/1oD9Z0VMz-l0DHpFxPu1oSyIhshzPu5Mk/edit?usp=sharing&ouid=105607031437751611507&rtpof=true&sd=true)
- [Figma Design](https://www.figma.com/design/vpXG6EV3bQxsLMF8JYRGjV/capstone?node-id=0-1&t=Ahrr6lRoqB9Y1dUl-1)
- [FastAPI Docs](http://localhost:5001/docs)

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/uwituzeb/healthcare-facility-planning-capstone-project.git
cd healthcare-facility-planning-capstone-project

# 2. Configure environment
cp .env.template backend/.env

# 4. Install dependencies
cd backend && npm install
cd ../frontend-react/frontend && npm install
cd ../../ml-service && pip install -r requirements.txt

# 5. Export ML model 
python scripts/export_model.py

# 6. Start all services
./scripts/start_all_services.sh

# 7. Open browser
open http://localhost:3000
```

## Features

### 🗺️ Interactive Mapping
- View existing healthcare facilities across Rwanda
- Analyze district-level accessibility
- Visualize population density and travel times

### 🤖 ML-Powered Recommendations
- Satellite imagery analysis using Sentinel-2
- Built-up area detection with 98.9% accuracy
- Confidence scores for each recommendation
- Automatic fallback to LLM if ML unavailable

### 📊 Accessibility Analysis
- Calculate average travel times to nearest facility
- Identify underserved areas
- Compare against target accessibility goals

### 👥 User Management
- Role-based access control (Admin, Policymaker, Healthcare Professional, Researcher)
- Approval-based registration system
- Admin dashboard for user management


## Architecture

```
┌─────────────────┐
│  Frontend       │  React, Mapbox GL, Tailwind CSS
│  (ReactJS)        │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Backend        │  Node.js, Express (Port 8080)
│  (NodeJS)      │
└────┬─────────┬──┘
     │         │
     ↓         ↓
┌────────┐  ┌──────────────┐
│ ML     │  │  Database    │
│Service │  │  (Supabase)  │
│(FastAPI│  │  PostgreSQL  │
│        │  │  + PostGIS)  │
└────────┘  └──────────────┘
```

### Tech Stack

**Frontend:** ReactJS, Tailwind CSS, React Router
**Backend:** Node.js, Express, Supabase Client
**ML Service:** Python, FastAPI, Google Earth Engine
**Database:** Supabase (PostgreSQL + PostGIS)


## Project Structure

```
healthcare-facility-finder/
├── backend/                # Node.js Express API
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic (LLM, ML)
│   └── lib/                # Utilities
├── frontend-react/         # React frontend
│   └── frontend/
│       ├── src/
│       │   ├── components/
│       │   ├── lib/        
│       │   └── pages/    
│       └── public/
├── ml-service/       
│   ├── app/                # FastAPI application
│   ├── models/             # Trained models
│   └── requirements.txt
├── scripts/                # Utility scripts
│   ├── start_all_services.sh
│   ├── train_model.py
│   ├── export_model.py
│   └── download_data_simple.py
├── supabase/              # Database migrations
│   └── migrations/
├── .env.template          # Environment template
├── SUPABASE_SETUP.sql     # Database setup script for supabase
└── README.md              
```

## API Endpoints

### Analysis
- `GET /api/analyze?district={name}&targetTravel={minutes}` - Analyze district accessibility

### Recommendations
- `POST /api/recommend` - Get ML-powered facility recommendations
- `GET /api/recommend/history/:districtId` - View recommendation history

### ML Service
- `GET /api/ml/health` - ML service health check
- `POST /api/ml/predict` - Direct ML prediction from features
- `POST /api/ml/predict-from-location` - Predict from coordinates

### Health
- `GET /api/health` - Backend health check

**Full API documentation:** [FastAPI Docs](http://localhost:5001/docs) (when ML service running)

## ML Model Details

### Model Type
Random Forest Classifier (200 estimators)

### Training Data
- **Source:** Sentinel-2 satellite imagery
- **Labels:** ESA WorldCover 2021
- **Region:** Rwanda
- **Resolution:** 10 meters

### Features (12 total)
RGB statistics, NDVI (vegetation), Built-up index, Brightness

### Performance
- **Accuracy:** 98.93%
- **Precision:** 0.99
- **Recall:** 0.98
- **F1-Score:** 0.98

---

## Development

### Running Services Individually

**Backend:**
```bash
cd backend
npm install
npm start  # Port 8080
```

**Frontend:**
```bash
cd frontend-react/frontend
npm install
npm start  # Port 3000
```

**ML Service:**
```bash
cd ml-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app.main  # Port 5001
```

## Deployment

### Docker Compose

```bash
docker-compose up --build
```

### Cloud Run (Google Cloud)

```bash
# Deploy backend
gcloud run deploy backend --source ./backend --region us-central1

# Deploy ML service
gcloud run deploy ml-service --source ./ml-service --region us-central1

# Deploy frontend
gcloud run deploy frontend --source ./frontend-react/frontend --region us-central1
```

## Acknowledgments

- **Sentinel-2** satellite imagery from ESA Copernicus program
- **ESA WorldCover** for land cover classification
- **Google Earth Engine** for geospatial data processing
- **Supabase** for backend infrastructure
- **Mapbox** for mapping visualization


## Roadmap

### Phase 1 (Current)
- ✅ ML-powered recommendations
- ✅ District-level analysis
- ✅ Admin approval system for security and privacy

### Phase 2 (Planned)
- Real-time satellite updates
- Multi-country support
- Advanced analytics dashboard
- Mobile app (React Native)

### Phase 3 (Future)
- Population forecasting
- Cost estimation models
- Integration with national health systems
- Automated facility placement optimization


## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b ft/feature-description`
3. Commit changes: `git commit -m 'New feature'`
4. Push to branch: `git push origin ft/feature-description`
5. Open Pull Request
