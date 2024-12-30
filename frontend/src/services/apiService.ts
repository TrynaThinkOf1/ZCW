import axios from "axios";

const api = axios.create({
  baseURL: "http://45.79.216.238:5001/api",
  headers: {"Content-Type": "application/json"},
});

export const verifyEmail = async (email: string) => {
  const response = await api.get(`/user/verify/${email}`);
  return response.data;
};

export const verifyCode = async (code: string, payload: any) => {
  const response = await api.post(`/code/verify/${code}`, payload);
  return response.data;
};

export const getUser = async () => {
  const token = localStorage.getItem("jwt"); // Retrieve token from localStorage
  if (!token) {
    throw new Error("No token found. Please log in.");
  }

  const response = await api.get("/user/get");
  return response.data;
};

export const login = async (payload: any) => {
  const response = await api.post("/user/login", payload)
  return response.data;
}

export const updateUser = async (payload: any) => {
  const token = localStorage.getItem("jwt");
  if (!token) {
    throw new Error("No token found. Please log in.");
  }
  console.log(payload);
  console.log(token);

  const response = await api.patch(`/user/update`, payload)
  console.log(response.data);
  return response.data;
}