import axios from "axios";

const api = axios.create({
  baseURL: "http://45.79.216.238:5001/api",
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("jwt");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Exported Functions
export const verifyEmail = async (email: string) => {
  const response = await api.get(`/user/verify/${email}`);
  return response.data;
};

export const verifyCode = async (code: string, payload: any) => {
  const response = await api.post(`/code/verify/${code}`, payload);
  return response.data;
};

export const getUser = async () => {
  try {
    const response = await api.get("/user/get");
    return response.data;
  } catch (error) {
    handleAuthError(error);
    throw error;
  }
};

export const login = async (payload: any) => {
  const response = await api.post("/user/login", payload);
  if (response.data && response.data.token) {
    localStorage.setItem("jwt", response.data.token);
  }
  return response.data;
};

export const updateUser = async (payload: any) => {
  try {
    const response = await api.patch(`/user/update`, payload);
    return response.data;
  } catch (error) {
    handleAuthError(error);
    throw error;
  }
};

const handleAuthError = (error: any) => {
  if (error.response && error.response.status === 401) {
    localStorage.removeItem("jwt");
    alert("Session expired. Please log in again.");
    window.location.href = "/login";
  }
};
