import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Device } from '../../types/device';
import { deviceApi } from '../../api/deviceApi';

export const DeviceList: React.FC = () => {
    const [devices, setDevices] = useState<Device[]>([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchDevices = async () => {
            try {
                const data = await deviceApi.getDevices();
                setDevices(data);
            } catch (error) {
                console.error('デバイス一覧の取得に失敗しました:', error);
            }
        };

        fetchDevices();
    }, []);

    const handleEdit = (id: string) => {
        navigate(`/devices/edit/${id}`);
    };

    const handleCreate = () => {
        navigate('/devices/create');
    };

    return (
        <div>
            <h1>機器一覧</h1>
            <button onClick={handleCreate}>新規登録</button>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>機器名</th>
                        <th>メーカー</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    {devices.map((device) => (
                        <tr key={device.id}>
                            <td>{device.id}</td>
                            <td>{device.name}</td>
                            <td>{device.manufacturer}</td>
                            <td>
                                <button onClick={() => handleEdit(device.id)}>
                                    編集
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}; 