import api from './client.js';

export const listDoctors     = (params)   => api.get('/doctors/doctors/', { params }).then((r) => r.data);
export const getDoctor       = (id)       => api.get(`/doctors/doctors/${id}/`).then((r) => r.data);
export const createDoctor    = (data)     => api.post('/doctors/doctors/', data).then((r) => r.data);
export const updateDoctor    = (id, data) => api.patch(`/doctors/doctors/${id}/`, data).then((r) => r.data);
export const deleteDoctor    = (id)       => api.delete(`/doctors/doctors/${id}/`);

export const listSpecialties     = () => api.get('/doctors/specialties/').then((r) => r.data);
export const listQualifications  = () => api.get('/doctors/qualifications/').then((r) => r.data);
