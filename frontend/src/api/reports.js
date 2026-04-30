import api from './client.js';

export const getDashboardKPI = () => api.get('/reports/dashboard/').then((r) => r.data);
export const getRevenue      = () => api.get('/reports/revenue/').then((r) => r.data);
export const getTopDoctors   = () => api.get('/reports/top-doctors/').then((r) => r.data);
export const getSpecialtyDistribution = () => api.get('/reports/specialty-distribution/').then((r) => r.data);
export const getDiscountDistribution  = () => api.get('/reports/discount-distribution/').then((r) => r.data);
