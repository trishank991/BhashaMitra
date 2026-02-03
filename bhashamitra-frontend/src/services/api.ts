/**
 * Base API Client Configuration
 *
 * Configures axios instance with authentication, base URL, and error handling.
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

// API base URL - Production default (v2)
// For local dev: set NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 in .env.local
const PRODUCTION_API = 'https://bhashamitra.onrender.com/api/v1';
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || PRODUCTION_API;

// Create axios instance with base configuration
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - adds auth token to requests
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Get token from localStorage (or your auth store)
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handles errors and token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // Handle 401 Unauthorized - attempt token refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          localStorage.setItem('access_token', access);

          // Retry original request with new token
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${access}`;
          }
          return apiClient(originalRequest);
        }
      } catch {
        // Refresh failed - clear tokens and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');

        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
      }
    }

    return Promise.reject(error);
  }
);

// API Error type for consistent error handling
export interface ApiError {
  message: string;
  status: number;
  errors?: Record<string, string[]>;
}

// Helper to extract error message from axios error
export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail?: string; message?: string }>;
    return (
      axiosError.response?.data?.detail ||
      axiosError.response?.data?.message ||
      axiosError.message ||
      'An unexpected error occurred'
    );
  }
  return 'An unexpected error occurred';
}

export default apiClient;
