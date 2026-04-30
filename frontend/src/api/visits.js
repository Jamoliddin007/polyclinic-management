import api from './client.js';

export const listVisits        = (params)   => api.get('/visits/visits/', { params }).then((r) => r.data);
export const getVisit          = (id)       => api.get(`/visits/visits/${id}/`).then((r) => r.data);
export const createVisit       = (data)     => api.post('/visits/visits/', data).then((r) => r.data);
export const updateVisit       = (id, data) => api.patch(`/visits/visits/${id}/`, data).then((r) => r.data);
export const deleteVisit       = (id)       => api.delete(`/visits/visits/${id}/`);

export const recalculateVisit  = (id) => api.post(`/visits/visits/${id}/recalculate/`).then((r) => r.data);
export const markVisitPaid     = (id) => api.post(`/visits/visits/${id}/mark_paid/`).then((r) => r.data);
export const cancelVisit       = (id) => api.post(`/visits/visits/${id}/cancel/`).then((r) => r.data);

export const listProcedureTypes = () =>
  api.get('/visits/procedure-types/').then((r) => r.data);
