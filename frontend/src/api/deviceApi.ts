import axios from 'axios';
import { Device, DeviceCreateInput, DeviceUpdateInput } from '../types/device';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_PATH = '/api/v1/devices';

export const deviceApi = {
    // デバイス一覧の取得
    getDevices: async (): Promise<Device[]> => {
        const response = await axios.get(`${API_BASE_URL}${API_PATH}/`);
        return response.data;
    },

    // 特定のデバイスの取得
    getDevice: async (id: string): Promise<Device> => {
        const response = await axios.get(`${API_BASE_URL}${API_PATH}/${id}`);
        return response.data;
    },

    // デバイスの作成
    createDevice: async (device: DeviceCreateInput): Promise<Device> => {
        const response = await axios.post(`${API_BASE_URL}${API_PATH}/`, device);
        return response.data;
    },

    // デバイスの更新
    updateDevice: async (id: string, device: DeviceUpdateInput): Promise<Device> => {
        const response = await axios.put(`${API_BASE_URL}${API_PATH}/${id}`, device);
        return response.data;
    },

    // デバイスの削除
    deleteDevice: async (id: string): Promise<void> => {
        await axios.delete(`${API_BASE_URL}${API_PATH}/${id}`);
    }
}; 