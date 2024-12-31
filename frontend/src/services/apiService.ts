import axios from 'axios';
import {config} from "typescript-eslint";

const api = axios.create({
  baseURL: 'http://45.79.216.238:5001/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true
});

const saveData = (data: any) => {
  try {
    for (const key in data) {
      localStorage.setItem(key, JSON.stringify(data[key]));
      console.log(`${key}: ${localStorage.getItem(key)}`);
    }
  } catch (error: any) {
    console.error("Error saving data to localStorage:", error);
  }
};

api.interceptors.response.use(
  (response) => response,
  (error: any) => {
    if (error.response?.status === 401) {
      console.warn("Session expired, redirecting to login...");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
api.interceptors.request.use((config) => {
  console.log('Sending request with cookies:', document.cookie);
  return config;
})

export const verifyEmail = async (email: string) => {
  try {
    const response = await api.get(`/user/verify/${email}`);
    return response.data;
  } catch (error: any) {
    console.error("Error verifying email:", error.response?.data || error.message);
    throw error;
  }
};

export const verifyCode = async (code: string, payload: any) => {
  try {
    const response = await api.post(`/code/verify/${code}`, payload);
    saveData(response.data);
    return response.data;
  } catch (error: any) {
    console.error("Error verifying code:", error.response?.data || error.message);
    throw error;
  }
};

export const loginUser = async (email: string, passkey: string) => {
  try {
    const response = await api.post('/user/login', { email, passkey });
    console.log('User logged in:', response.data);
    saveData({ email, ...response.data });
    return response.data;
  } catch (error: any) {
    console.error('Login failed:', error.response?.data || error.message);
    throw error;
  }
};


export const updateUser = async (data: any) => {
  try {
    const email = JSON.parse(localStorage.getItem("email") || 'null');
    if (!email) {
      throw new Error("Email not found in localStorage. Please log in again.");
    }
    data["email"] = email;

    const response = await api.patch('/user/update', data);
    console.log('User updated:', response.data);
    saveData(response.data);
    return response.data;
  } catch (error: any) {
    console.error('Update failed:', error.response?.data || error.message);
    throw error;
  }
};


export const getUserData = async (email: string) => {
  try {
    const response = await api.post('/user/get', { email });
    console.log('User data:', response.data);
    saveData(response.data);
    return response.data;
  } catch (error: any) {
    console.error('Error getting user data:', error.response?.data || error.message);
    throw error;
  }
};
