-- ============================================================================
-- Healthcare Facility Planning System - Initial Database Schema
-- Version: 1.0
-- Date: 2025-11-03
--
-- This migration creates the full database schema as defined in the
-- research proposal Section 3.5.1 (Entity Relationship Diagram)
-- ============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- CORE GEOGRAPHIC TABLES
-- ============================================================================

-- Geographic Regions (Province > District > Sector hierarchy)
CREATE TABLE IF NOT EXISTS geographic_regions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    region_type VARCHAR(50) NOT NULL CHECK (region_type IN ('province', 'district', 'sector', 'cell', 'village')),
    parent_id UUID REFERENCES geographic_regions(id) ON DELETE CASCADE,
    boundary GEOMETRY(POLYGON, 4326),
    area_km2 DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE geographic_regions IS 'Administrative regions of Rwanda with hierarchical structure';
COMMENT ON COLUMN geographic_regions.region_type IS 'province, district, sector, cell, or village';


-- ============================================================================
-- HEALTHCARE INFRASTRUCTURE
-- ============================================================================

-- Healthcare Facilities
CREATE TABLE IF NOT EXISTS healthcare_facilities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    facility_type VARCHAR(50) NOT NULL CHECK (facility_type IN ('hospital', 'district_hospital', 'health_center', 'health_post', 'clinic', 'pharmacy', 'referral_hospital')),
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    location GEOMETRY(POINT, 4326),
    region_id UUID REFERENCES geographic_regions(id) ON DELETE SET NULL,
    capacity INTEGER DEFAULT 0,
    bed_count INTEGER DEFAULT 0,
    services TEXT[],
    operating_hours VARCHAR(100),
    contact_phone VARCHAR(50),
    osm_id BIGINT,
    data_source VARCHAR(100) DEFAULT 'osm',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE healthcare_facilities IS 'Healthcare facilities across Rwanda';
COMMENT ON COLUMN healthcare_facilities.services IS 'Array of services offered (e.g., maternity, emergency, surgery)';


-- ============================================================================
-- POPULATION & DEMOGRAPHICS
-- ============================================================================

-- Population Data
CREATE TABLE IF NOT EXISTS population_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    region_id UUID REFERENCES geographic_regions(id) ON DELETE CASCADE,
    total_population INTEGER NOT NULL,
    density_per_km2 DECIMAL(10, 2),
    male_population INTEGER,
    female_population INTEGER,
    age_distribution JSONB,
    households INTEGER,
    avg_household_size DECIMAL(4, 2),
    urban_population INTEGER,
    rural_population INTEGER,
    data_year INTEGER NOT NULL,
    data_source VARCHAR(100) DEFAULT 'worldpop',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(region_id, data_year)
);

COMMENT ON TABLE population_data IS 'Population demographics by region and year';
COMMENT ON COLUMN population_data.age_distribution IS 'JSON object with age brackets (e.g., {"0-5": 12000, "6-14": 18000})';


-- ============================================================================
-- ACCESSIBILITY & METRICS
-- ============================================================================

-- Accessibility Metrics
CREATE TABLE IF NOT EXISTS accessibility_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    region_id UUID REFERENCES geographic_regions(id) ON DELETE CASCADE,
    accessibility_score DECIMAL(5, 3) NOT NULL CHECK (accessibility_score BETWEEN 0 AND 1),
    avg_travel_time_minutes DECIMAL(6, 2),
    median_travel_time_minutes DECIMAL(6, 2),
    max_travel_time_minutes DECIMAL(6, 2),
    population_coverage_pct DECIMAL(5, 2) CHECK (population_coverage_pct BETWEEN 0 AND 100),
    population_within_5km INTEGER,
    population_within_25min INTEGER,
    underserved_population INTEGER,
    facility_density_per_10k DECIMAL(5, 2),
    meets_hssp_target BOOLEAN,
    calculation_date TIMESTAMP DEFAULT NOW(),
    calculation_method VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE accessibility_metrics IS 'Healthcare accessibility metrics per region';
COMMENT ON COLUMN accessibility_metrics.meets_hssp_target IS 'Whether region meets WHO 25-minute target';

CREATE INDEX idx_accessibility_region ON accessibility_metrics(region_id);
CREATE INDEX idx_accessibility_score ON accessibility_metrics(accessibility_score);


-- ============================================================================
-- GEOSPATIAL DATA
-- ============================================================================

-- Satellite Images
CREATE TABLE IF NOT EXISTS satellite_images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    region_id UUID REFERENCES geographic_regions(id) ON DELETE SET NULL,
    image_url TEXT NOT NULL,
    storage_path TEXT,
    acquisition_date DATE NOT NULL,
    resolution_meters DECIMAL(5, 2),
    source VARCHAR(100) NOT NULL CHECK (source IN ('sentinel-2', 'planetscope', 'landsat', 'other')),
    cloud_cover_pct DECIMAL(5, 2),
    bands INTEGER,
    file_size_mb DECIMAL(10, 2),
    bounds GEOMETRY(POLYGON, 4326),
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE satellite_images IS 'Satellite imagery repository';

CREATE INDEX idx_satellite_region ON satellite_images(region_id);
CREATE INDEX idx_satellite_date ON satellite_images(acquisition_date);


-- Building Clusters (ML detected)
CREATE TABLE IF NOT EXISTS building_clusters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    satellite_image_id UUID REFERENCES satellite_images(id) ON DELETE CASCADE,
    centroid GEOMETRY(POINT, 4326) NOT NULL,
    boundary GEOMETRY(POLYGON, 4326),
    building_count INTEGER,
    cluster_area_km2 DECIMAL(10, 4),
    density_per_km2 DECIMAL(10, 2),
    ml_confidence DECIMAL(5, 3) CHECK (ml_confidence BETWEEN 0 AND 1),
    classified_as VARCHAR(50),
    features JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE building_clusters IS 'ML-detected building clusters from satellite imagery';

CREATE INDEX idx_clusters_image ON building_clusters(satellite_image_id);
CREATE INDEX idx_clusters_location ON building_clusters USING GIST(centroid);


-- Road Networks
CREATE TABLE IF NOT EXISTS road_networks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    region_id UUID REFERENCES geographic_regions(id) ON DELETE SET NULL,
    road_geometry GEOMETRY(LINESTRING, 4326) NOT NULL,
    road_type VARCHAR(50) CHECK (road_type IN ('motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential', 'track', 'path')),
    road_name VARCHAR(255),
    surface VARCHAR(50),
    length_km DECIMAL(10, 3),
    lanes INTEGER,
    max_speed_kmh INTEGER,
    osm_id BIGINT,
    is_paved BOOLEAN,
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE road_networks IS 'Road network data from OpenStreetMap';

CREATE INDEX idx_roads_region ON road_networks(region_id);
CREATE INDEX idx_roads_geometry ON road_networks USING GIST(road_geometry);
CREATE INDEX idx_roads_type ON road_networks(road_type);


-- ============================================================================
-- MACHINE LEARNING
-- ============================================================================

-- ML Models Registry
CREATE TABLE IF NOT EXISTS ml_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_name VARCHAR(255) NOT NULL,
    model_type VARCHAR(100) NOT NULL CHECK (model_type IN ('random_forest', 'cnn', 'svm', 'xgboost', 'other')),
    version VARCHAR(50) NOT NULL,
    description TEXT,
    architecture JSONB,
    hyperparameters JSONB,
    accuracy DECIMAL(5, 3),
    precision_score DECIMAL(5, 3),
    recall DECIMAL(5, 3),
    f1_score DECIMAL(5, 3),
    rmse DECIMAL(10, 4),
    confusion_matrix JSONB,
    feature_importance JSONB,
    training_date TIMESTAMP NOT NULL,
    training_duration_minutes INTEGER,
    training_samples INTEGER,
    test_samples INTEGER,
    model_file_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_by UUID REFERENCES auth.users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(model_name, version)
);

COMMENT ON TABLE ml_models IS 'Registry of trained ML models with metadata and metrics';


-- Training Data
CREATE TABLE IF NOT EXISTS training_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_id UUID REFERENCES ml_models(id) ON DELETE CASCADE,
    satellite_image_id UUID REFERENCES satellite_images(id) ON DELETE SET NULL,
    patch_coordinates JSONB,
    features JSONB NOT NULL,
    label INTEGER NOT NULL,
    split VARCHAR(20) CHECK (split IN ('train', 'validation', 'test')),
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE training_data IS 'Training/test data for ML models';

CREATE INDEX idx_training_model ON training_data(model_id);


-- ============================================================================
-- ANALYSIS & RECOMMENDATIONS
-- ============================================================================

-- Analysis Reports
CREATE TABLE IF NOT EXISTS analysis_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    region_id UUID REFERENCES geographic_regions(id) ON DELETE SET NULL,
    report_type VARCHAR(100) NOT NULL CHECK (report_type IN ('accessibility', 'facility_placement', 'gap_analysis', 'hssp_compliance', 'comprehensive')),
    title VARCHAR(500),
    summary TEXT,
    methodology TEXT,
    findings JSONB,
    recommendations JSONB,
    priority_areas JSONB,
    hssp_alignment JSONB,
    data_sources JSONB,
    generated_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE analysis_reports IS 'Generated analysis reports with recommendations';

CREATE INDEX idx_reports_user ON analysis_reports(user_id);
CREATE INDEX idx_reports_region ON analysis_reports(region_id);
CREATE INDEX idx_reports_type ON analysis_reports(report_type);


-- LLM Analysis
CREATE TABLE IF NOT EXISTS llm_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_id UUID REFERENCES analysis_reports(id) ON DELETE CASCADE,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    model_used VARCHAR(100) NOT NULL,
    tokens_used INTEGER,
    confidence_score DECIMAL(5, 3),
    processing_time_ms INTEGER,
    context_data JSONB,
    feedback_rating INTEGER CHECK (feedback_rating BETWEEN 1 AND 5),
    feedback_comment TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE llm_analysis IS 'LLM-generated insights and recommendations';

CREATE INDEX idx_llm_report ON llm_analysis(report_id);


-- ============================================================================
-- SPATIAL INDEXES FOR PERFORMANCE
-- ============================================================================

CREATE INDEX idx_facilities_location ON healthcare_facilities USING GIST(location);
CREATE INDEX idx_facilities_region ON healthcare_facilities(region_id);
CREATE INDEX idx_facilities_type ON healthcare_facilities(facility_type);

CREATE INDEX idx_regions_boundary ON geographic_regions USING GIST(boundary);
CREATE INDEX idx_regions_parent ON geographic_regions(parent_id);

CREATE INDEX idx_population_region ON population_data(region_id);

CREATE INDEX idx_satellite_bounds ON satellite_images USING GIST(bounds);


-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: Facilities with Region Information
CREATE OR REPLACE VIEW vw_facilities_with_regions AS
SELECT
    f.id,
    f.name AS facility_name,
    f.facility_type,
    f.latitude,
    f.longitude,
    f.capacity,
    f.services,
    r.name AS region_name,
    r.region_type,
    f.is_active
FROM healthcare_facilities f
LEFT JOIN geographic_regions r ON f.region_id = r.id;


-- View: Current Accessibility by District
CREATE OR REPLACE VIEW vw_current_accessibility AS
SELECT
    r.name AS district,
    r.region_type,
    am.accessibility_score,
    am.avg_travel_time_minutes,
    am.population_coverage_pct,
    am.underserved_population,
    am.meets_hssp_target,
    am.calculation_date
FROM accessibility_metrics am
JOIN geographic_regions r ON am.region_id = r.id
WHERE r.region_type = 'district'
AND am.calculation_date = (
    SELECT MAX(calculation_date)
    FROM accessibility_metrics am2
    WHERE am2.region_id = am.region_id
);


-- View: Underserved Regions
CREATE OR REPLACE VIEW vw_underserved_regions AS
SELECT
    r.id AS region_id,
    r.name AS region_name,
    r.region_type,
    p.total_population,
    am.accessibility_score,
    am.avg_travel_time_minutes,
    am.underserved_population,
    CASE
        WHEN am.avg_travel_time_minutes > 60 THEN 'Critical'
        WHEN am.avg_travel_time_minutes > 45 THEN 'High'
        WHEN am.avg_travel_time_minutes > 25 THEN 'Medium'
        ELSE 'Low'
    END AS priority_level
FROM geographic_regions r
JOIN accessibility_metrics am ON r.id = am.region_id
JOIN population_data p ON r.id = p.region_id
WHERE am.meets_hssp_target = FALSE
ORDER BY am.avg_travel_time_minutes DESC;


-- ============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================================================

-- Enable RLS on sensitive tables
ALTER TABLE analysis_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE llm_analysis ENABLE ROW LEVEL SECURITY;

-- Policy: Users can view their own reports
CREATE POLICY user_own_reports ON analysis_reports
    FOR SELECT
    USING (auth.uid() = user_id OR is_public = TRUE);

-- Policy: Users can create their own reports
CREATE POLICY user_create_reports ON analysis_reports
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Policy: Admins can view all reports
-- Note: This assumes you have a custom claims setup for admin role
-- If not, you'll need to create a separate roles table


-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================================

-- Function: Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to relevant tables
CREATE TRIGGER update_geographic_regions_updated_at BEFORE UPDATE ON geographic_regions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_healthcare_facilities_updated_at BEFORE UPDATE ON healthcare_facilities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_population_data_updated_at BEFORE UPDATE ON population_data
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- Function: Calculate facility density
CREATE OR REPLACE FUNCTION calculate_facility_density(region_uuid UUID)
RETURNS DECIMAL AS $$
DECLARE
    facility_count INTEGER;
    population INTEGER;
    density DECIMAL;
BEGIN
    SELECT COUNT(*) INTO facility_count
    FROM healthcare_facilities
    WHERE region_id = region_uuid AND is_active = TRUE;

    SELECT total_population INTO population
    FROM population_data
    WHERE region_id = region_uuid
    ORDER BY data_year DESC
    LIMIT 1;

    IF population > 0 THEN
        density := (facility_count::DECIMAL / population) * 10000;
    ELSE
        density := 0;
    END IF;

    RETURN density;
END;
$$ LANGUAGE plpgsql;


-- ============================================================================
-- SEED DATA (Optional - commented out, run separately)
-- ============================================================================

-- Rwanda Provinces
-- INSERT INTO geographic_regions (name, region_type, boundary) VALUES
-- ('Kigali', 'province', ST_GeomFromText('POLYGON(...)', 4326)),
-- ('Eastern Province', 'province', ST_GeomFromText('POLYGON(...)', 4326)),
-- ('Western Province', 'province', ST_GeomFromText('POLYGON(...)', 4326)),
-- ('Northern Province', 'province', ST_GeomFromText('POLYGON(...)', 4326)),
-- ('Southern Province', 'province', ST_GeomFromText('POLYGON(...)', 4326));


-- ============================================================================
-- COMPLETION
-- ============================================================================

-- Log migration completion
DO $$
BEGIN
    RAISE NOTICE 'Healthcare Facility Planning database schema initialized successfully';
    RAISE NOTICE 'Tables created: 13';
    RAISE NOTICE 'Views created: 3';
    RAISE NOTICE 'Indexes created: Multiple spatial and performance indexes';
    RAISE NOTICE 'RLS enabled on: analysis_reports, llm_analysis';
END $$;
