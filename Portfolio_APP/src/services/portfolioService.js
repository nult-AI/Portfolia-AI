import apiClient from './apiClient';

/**
 * Utility to build query params
 */
const buildQuery = (params = {}) => {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== null && value !== undefined) {
      query.append(key, value);
    }
  });
  const queryString = query.toString();
  return queryString ? `?${queryString}` : '';
};

/**
 * Profile API Service
 */
export const profileService = {
  getProfile: (params) => apiClient.get(`/profile${buildQuery(params)}`),
  createProfile: (data) => apiClient.post('/profile', data),
  updateProfile: (id, data) => apiClient.put(`/profile/${id}`, data),
  deleteProfile: (id) => apiClient.delete(`/profile/${id}`),
};

/**
 * Skill Category API Service
 */
export const skillCategoryService = {
  getAll: (params) => 
    apiClient.get(`/skills/categories${buildQuery(params)}`),
  getById: (id) => apiClient.get(`/skills/categories/${id}`),
  create: (data) => apiClient.post('/skills/categories', data),
  update: (id, data) => apiClient.put(`/skills/categories/${id}`, data),
  delete: (id) => apiClient.delete(`/skills/categories/${id}`),
};

/**
 * Skill API Service
 */
export const skillService = {
  getAll: (categoryId = null) => {
    const query = categoryId ? `?category_id=${categoryId}` : '';
    return apiClient.get(`/skills${query}`);
  },
  create: (data) => apiClient.post('/skills', data),
  delete: (id) => apiClient.delete(`/skills/${id}`),
};

/**
 * Other Skill API Service
 */
export const otherSkillService = {
  getAll: (params) => apiClient.get(`/other-skills${buildQuery(params)}`),
  create: (data) => apiClient.post('/other-skills', data),
  update: (id, data) => apiClient.put(`/other-skills/${id}`, data),
  delete: (id) => apiClient.delete(`/other-skills/${id}`),
};

/**
 * Experience API Service
 */
export const experienceService = {
  getAll: (params) => apiClient.get(`/experience${buildQuery(params)}`),
  getById: (id) => apiClient.get(`/experience/${id}`),
  create: (data) => apiClient.post('/experience', data),
  update: (id, data) => apiClient.put(`/experience/${id}`, data),
  delete: (id) => apiClient.delete(`/experience/${id}`),
};

/**
 * Education API Service
 */
export const educationService = {
  getAll: (params) => apiClient.get(`/education${buildQuery(params)}`),
  getById: (id) => apiClient.get(`/education/${id}`),
  create: (data) => apiClient.post('/education', data),
  update: (id, data) => apiClient.put(`/education/${id}`, data),
  delete: (id) => apiClient.delete(`/education/${id}`),
};

/**
 * CV Extraction API Service
 */
export const cvService = {
  process: (file, mode = 'preview') => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('mode', mode);
    return apiClient.post('/cv/process', formData);
  },
};

/**
 * Auth API Service
 */
export const authService = {
  googleLogin: (token) => apiClient.post('/auth/google-login', { token }),
};
