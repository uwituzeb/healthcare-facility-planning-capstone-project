// src/services/api.js
// Healthcare API Service - Updated to work with Flask backend

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class HealthcareAPI {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  /**
   * Generic fetch wrapper with error handling
   */
  async fetchAPI(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'API request failed');
      }

      return data;
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  /**
   * Dashboard Statistics
   */
  async getDashboardStats() {
    return this.fetchAPI('/dashboard/stats');
  }

  /**
   * Get all districts data
   * @param {string} province - Optional province filter (all, kigali, eastern, etc.)
   */
  async getDistricts(province = 'all') {
    const endpoint = province === 'all' 
      ? '/districts' 
      : `/districts?province=${province}`;
    return this.fetchAPI(endpoint);
  }

  /**
   * Get specific district details
   * @param {string} districtName - Name of the district
   */
  async getDistrictDetail(districtName) {
    return this.fetchAPI(`/districts/${districtName}`);
  }

  /**
   * Get facility placement recommendations
   * @param {number} limit - Number of recommendations to retrieve
   */
  async getRecommendations(limit = 10) {
    return this.fetchAPI(`/recommendations?limit=${limit}`);
  }

  /**
   * Get province summaries
   */
  async getProvinces() {
    return this.fetchAPI('/provinces');
  }

  /**
   * Get accessibility analysis
   * @param {string} province - Optional province filter
   */
  async getAccessibilityAnalysis(province = 'all') {
    const endpoint = province === 'all'
      ? '/accessibility'
      : `/accessibility?province=${province}`;
    return this.fetchAPI(endpoint);
  }

  /**
   * Get underserved areas
   * @param {number} limit - Number of areas to retrieve
   */
  async getUnderservedAreas(limit = 10) {
    return this.fetchAPI(`/underserved?limit=${limit}`);
  }

  /**
   * Get priority areas for intervention
   */
  async getPriorities() {
    return this.fetchAPI('/priorities');
  }

  /**
   * Get HSSP V targets progress
   */
  async getHSSPTargets() {
    return this.fetchAPI('/hssp-targets');
  }

  /**
   * Get recent analysis records
   */
  async getRecentAnalysis() {
    return this.fetchAPI('/analysis/recent');
  }

  /**
   * Get all healthcare facilities
   */
  async getFacilities() {
    return this.fetchAPI('/facilities');
  }

  /**
   * Export data
   * @param {string} format - Export format ('json' or 'csv')
   */
  async exportData(format = 'json') {
    return this.fetchAPI(`/export?format=${format}`);
  }

  /**
   * Health check
   */
  async healthCheck() {
    return this.fetchAPI('/health');
  }
}

// Create singleton instance
const api = new HealthcareAPI();

// Export both the instance and the class
export default api;
export { HealthcareAPI };

// Export individual methods
export const getDashboardStats = () => api.getDashboardStats();
export const getDistricts = (province) => api.getDistricts(province);
export const getDistrictDetail = (name) => api.getDistrictDetail(name);
export const getRecommendations = (limit) => api.getRecommendations(limit);
export const getProvinces = () => api.getProvinces();
export const getAccessibilityAnalysis = (province) => api.getAccessibilityAnalysis(province);
export const getUnderservedAreas = (limit) => api.getUnderservedAreas(limit);
export const getPriorities = () => api.getPriorities();
export const getHSSPTargets = () => api.getHSSPTargets();
export const getRecentAnalysis = () => api.getRecentAnalysis();
export const getFacilities = () => api.getFacilities();
export const exportData = (format) => api.exportData(format);
export const healthCheck = () => api.healthCheck();