import axios from "axios";

const API_BASE_URL: string = "http://45.79.216.238:5001/api";

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json"
    }
});

export const verifyEmail = async (email: string) => {
    const response = await api.get(`/users/verify/${email}`);
    return response.data;
};

export const verifyCode = async (code: string, payload) => {
    const response = await api.post(`/code/verify/${code}`, payload);
    return response.data;
};

export default api;