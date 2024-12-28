import axios from "axios";

type VerifyCodePayload = {
    passkey: string;
    email: string;
    firstName: string;
    lastName: string;
    displayName: string;
};

const API_BASE_URL = "http://45.79.216.238:5001/api";

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

export const verifyEmail = async (email: string) => {
    const response = await api.get(`/user/verify/${email}`);
    return response.data;
};

export const verifyCode = async (code: string, payload: VerifyCodePayload) => {
    const response = await api.post(`/code/verify/${code}`, payload);
    return response.data;
};

export default api;
