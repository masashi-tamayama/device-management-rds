import { useEffect, useState } from 'react';
import { Box, Button, Typography, Stack, Alert, Snackbar } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Table } from '../../components/common/Table';
import { Device } from '../../types/device';
import apiClient from '../../api/client';
import { Column } from '../../components/common/Table/types';
import { Dialog } from '../../components/common/Dialog';

export const DeviceList = () => {
  const navigate = useNavigate();
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Device | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

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

  const handleDelete = async () => {
    if (!deleteTarget) return;
    
    setDeleteLoading(true);
    try {
      await apiClient.delete(`/api/v1/devices/${deleteTarget.id}`);
      await fetchDevices();
      setDeleteTarget(null);
      setSuccessMessage(`${deleteTarget.name}を削除しました`);
    } catch (err) {
      console.error('Error deleting device:', err);
      setError('デバイスの削除に失敗しました');
    } finally {
      setDeleteLoading(false);
    }
  };

  const columns: Column<Device>[] = [
    { field: 'name' as keyof Device, headerName: '機器名', width: 200 },
    { field: 'manufacturer' as keyof Device, headerName: 'メーカー', width: 200 },
    {
      field: 'actions' as keyof Device,
      headerName: '操作',
      width: 200,
      renderCell: (row: Device) => (
        <Stack direction="row" spacing={1}>
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
          <Button
            variant="contained"
            color="error"
            size="small"
            onClick={(e) => {
              e.stopPropagation();
              setDeleteTarget(row);
            }}
          >
            削除
          </Button>
        </Stack>
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

      <Dialog
        open={!!deleteTarget}
        title="機器の削除"
        confirmText="削除"
        confirmVariant="danger"
        loading={deleteLoading}
        onConfirm={handleDelete}
        onCancel={() => setDeleteTarget(null)}
      >
        <Typography>
          {deleteTarget?.name}を削除してもよろしいですか？
          <br />
          この操作は取り消せません。
        </Typography>
      </Dialog>

      <Snackbar
        open={!!successMessage}
        autoHideDuration={3000}
        onClose={() => setSuccessMessage(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={() => setSuccessMessage(null)} severity="success">
          {successMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
}; 