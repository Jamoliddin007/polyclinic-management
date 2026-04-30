import api from './client.js';

export const listPatients   = (params)       => api.get('/patients/patients/', { params }).then((r) => r.data);
export const getPatient     = (id)           => api.get(`/patients/patients/${id}/`).then((r) => r.data);
export const createPatient  = (data)         => api.post('/patients/patients/', data).then((r) => r.data);
export const updatePatient  = (id, data)     => api.patch(`/patients/patients/${id}/`, data).then((r) => r.data);
export const deletePatient  = (id)           => api.delete(`/patients/patients/${id}/`);

export const listDiscountCategories = () =>
  api.get('/patients/discount-categories/').then((r) => r.data);
