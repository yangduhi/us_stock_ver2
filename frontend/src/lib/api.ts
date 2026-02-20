import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
});

export const fetchDashboardOverview = async () => {
    const { data } = await axiosInstance.get('/dashboard/overview');
    return data;
};

export const fetchAIIntelligence = async () => {
    const { data } = await axiosInstance.get('/dashboard/ai-intelligence');
    return data;
};

export const fetchTickerAnalysis = async (symbol: string) => {
    const { data } = await axiosInstance.get(`/market/tickers/${symbol}/analysis`);
    return data;
};

export const fetchTickerHistory = async (symbol: string, period: string = "1mo") => {
    const { data } = await axiosInstance.get(`/market/tickers/${symbol}/history`, { params: { period } });
    return data;
};
