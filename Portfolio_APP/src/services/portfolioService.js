import apiClient from './apiClient';

/**
 * Profile API Service
 */
export const profileService = {
  getProfile: () => apiClient.get('/profile'),
  createProfile: (data) => apiClient.post('/profile', data),
  updateProfile: (id, data) => apiClient.put(`/profile/${id}`, data),
  deleteProfile: (id) => apiClient.delete(`/profile/${id}`),
};

/**
 * Skill Category API Service
 */
export const skillCategoryService = {
  getAll: (includeInactive = false) => 
    apiClient.get(`/skills/categories?include_inactive=${includeInactive}`),
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
  getAll: () => apiClient.get('/other-skills'),
  create: (data) => apiClient.post('/other-skills', data),
  update: (id, data) => apiClient.put(`/other-skills/${id}`, data),
  delete: (id) => apiClient.delete(`/other-skills/${id}`),
};

/**
 * Experience API Service
 */
export const experienceService = {
  getAll: () => apiClient.get('/experience'),
  getById: (id) => apiClient.get(`/experience/${id}`),
  create: (data) => apiClient.post('/experience', data),
  update: (id, data) => apiClient.put(`/experience/${id}`, data),
  delete: (id) => apiClient.delete(`/experience/${id}`),
};

/**
 * Education API Service
 */
export const educationService = {
  getAll: () => apiClient.get('/education'),
  getById: (id) => apiClient.get(`/education/${id}`),
  create: (data) => apiClient.post('/education', data),
  update: (id, data) => apiClient.put(`/education/${id}`, data),
  delete: (id) => apiClient.delete(`/education/${id}`),
};
