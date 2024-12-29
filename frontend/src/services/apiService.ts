import axios from "axios";

const api = axios.create({
  baseURL: "http://45.79.216.238:5001/api"
});

// Endpoint: Verify Email
export const verifyEmail = async (email: string) => {
  const response = await api.get(`/user/verify/${email}`);
  return response.data;
};

export const verifyCode = async (code: string, payload: any) => {
  const response = await api.post(`/code/verify/${code}`, payload);
  return response.data;
};

export const getUser = async (token: string) => {
  const response = await api.get("/user/get", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

// Additional API endpoints can be added here as needed
