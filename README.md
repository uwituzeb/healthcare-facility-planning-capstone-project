# Healthcare Facility Planning Capstone Project

## Overview

This project aims to create an ML-driven web application to guide policymakers in healthcare facility planning placement. The initial implementation (demo) uses Google Earth Engine (GEE) and Python to process Sentinel-2 satellite imagery and ESA WorldCover data for Rwanda, focusing on land cover analysis and built-up area classification. It includes data preprocessing, visualization, and machine learning to identify built-up regions.

## Useful Links

- [Google Colab](https://colab.research.google.com/drive/14DFmzp2NZUoD-YDjNYutxfCC8dWomqqi?usp=sharing)
- [Research Proposal](https://docs.google.com/document/d/1oD9Z0VMz-l0DHpFxPu1oSyIhshzPu5Mk/edit?usp=sharing&ouid=105607031437751611507&rtpof=true&sd=true)
- [Github Link](https://github.com/uwituzeb/healthcare-facility-planning-capstone-project)
- [Figma Link](https://www.figma.com/design/vpXG6EV3bQxsLMF8JYRGjV/capstone?node-id=0-1&t=Ahrr6lRoqB9Y1dUl-1)

## Features

- **Data Visualization**: RGB composite images and histograms of Sentinel-2 bands (Red, Green, Blue).
- **Data Engineering**: Preparation of RGB pixel data for clustering.
- Tiles imagery into patches and trains a Random Forest classifier to detect built-up areas.
- Classification report for metrics

## Requirements

- Google Earth Engine API
- Python libraries: ee, geemap, rasterio, numpy, matplotlib, scikit-learn, patchify, scikit-image
- Google Drive access for exporting data
- Python environment with necessary dependencies installed

## Setup Project

1. Clone the repository

```
git clone https://github.com/uwituzeb/healthcare-facility-planning-capstone-project.git
```

2. Setup virtual environment

```
python -m venv venv
source venv/Scripts/activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run the cells to load sentinel-2 data, perform K-Means clustering and visualizations

## Data

- **Source**: Sentinel-2 imagery (2025-01-01 to 2025-09-30) from Google Earth Engine.
- **ESA WorldCover**: ESA/WorldCover/v200/2021 for land cover labels.
- **Export**: GeoTIFF files stored in Google Drive or local directory.

## Future Work

- Address class imbalance with oversampling or class weights.
- Collect more built-up area data for better model training.
- Enhance feature engineering for improved classification.
- Develop frontend and integrate with Flask API
- Optimize for larger datasets
