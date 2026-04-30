import api from './client.js';

export const login = async (username, password) => {
  const { data } = await api.post('/auth/login/', { username, password });
  return data;
};

export const refresh = async (refreshToken) => {
  const { data } = await api.post('/auth/refresh/', { refresh: refreshToken });
  return data;
};
