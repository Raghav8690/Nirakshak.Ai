import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getCustomers = () => api.get('/customers/');
export const getCustomer360 = (id) => api.get(`/customers/${id}`);
export const getTransactions = (customerId) => api.get(`/transactions/?customer_id=${customerId}`);
export const getTriggers = (customerId = '') => {
  const url = customerId ? `/triggers/?customer_id=${customerId}` : '/triggers/';
  return api.get(url);
};
export const scanTriggers = (customerId) => api.post('/triggers/scan', { customer_id: customerId });
export const submitFeedback = (triggerId, customerId, action) => 
  api.post('/feedback/', { trigger_id: triggerId, customer_id: customerId, action });
export const getAnalytics = () => api.get('/analytics/overview');
export const evaluateReasoning = (customerId, signal) => 
  api.post('/reasoning/evaluate', { customer_id: customerId, signal });

export default api;
