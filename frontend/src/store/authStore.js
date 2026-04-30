import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      user: null,

      setTokens: (access, refresh) => set({ accessToken: access, refreshToken: refresh }),
      setUser: (user) => set({ user }),

      login: (access, refresh, user) =>
        set({ accessToken: access, refreshToken: refresh, user }),

      logout: () => set({ accessToken: null, refreshToken: null, user: null }),

      isAuthenticated: () => {
        const state = JSON.parse(localStorage.getItem('auth-storage'))?.state;
        return !!state?.accessToken;
      },
    }),
    { name: 'auth-storage' },
  ),
);
