import { useEffect, useState } from 'react';
import { Box, Button, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Table } from '../../components/common/Table';
import { Device } from '../../types/device';
import apiClient from '../../api/client';
import { Column } from '../../components/common/Table/types';

export const DeviceList = () => {
  const navigate = useNavigate();
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDevices = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get('/api/v1/devices/');
      setDevices(response.data);
    } catch (err) {
      setError('デバイスの取得に失敗しました');
      console.error('Error fetching devices:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDevices();
  }, []);

  const columns: Column<Device>[] = [
    { field: 'name' as keyof Device, headerName: '機器名', width: 200 },
    { field: 'manufacturer' as keyof Device, headerName: 'メーカー', width: 200 },
    {
      field: 'actions' as keyof Device,
      headerName: '操作',
      width: 120,
      renderCell: (row: Device) => (
        <Button
          variant="contained"
          size="small"
          onClick={(e) => {
            e.stopPropagation();
            navigate(`/devices/${row.id}/edit`);
          }}
        >
          編集
        </Button>
      ),
    },
  ];

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" gutterBottom>
          機器一覧
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/devices/new')}
        >
          新規登録
        </Button>
      </Box>

      <Table
        columns={columns}
        rows={devices}
        loading={loading}
        error={error || undefined}
      />
    </Box>
  );
}; 