import axios from 'axios';

/**
 * Create an axios instance with a base URL for our backend API.
 * In a real application, this URL would come from an environment variable.
 */
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * We will assume the parent portal passes an auth token.
 * This function allows us to set it for all subsequent requests.
 * In a real app, this would be called once when the module initializes.
 */
export const setAuthToken = (token) => {
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete apiClient.defaults.headers.common['Authorization'];
  }
};

export default apiClient;
