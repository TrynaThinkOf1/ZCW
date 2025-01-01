import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true
});

interface loginResponse {
  user: any,
  pfp: string,
}

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
  console.log('Request Cookies:', document.cookie);
  return config;
});

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

export const loginUser = async (email: string, passkey: string): Promise<loginResponse> => {
  const response = await api.post<loginResponse>("/user/login", { email, passkey });
  return response.data;
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


export const fetchUserProfile = async (email: string): Promise<any> => {
  const response = await api.post("/user/get", { email });
  return response.data;
};