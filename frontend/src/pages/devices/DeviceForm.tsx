import { useEffect, useState } from 'react';
import { Box, Typography, Stack, Alert, Snackbar } from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import { TextField } from '../../components/common/TextField';
import { Button } from '../../components/common/Button';
import { Device, DeviceCreate } from '../../types/device';
import apiClient from '../../api/client';
import { Dialog } from '../../components/common/Dialog';

export const DeviceForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [showCancelDialog, setShowCancelDialog] = useState(false);
  const [formData, setFormData] = useState<DeviceCreate>({
    name: '',
    manufacturer: '',
  });
  const [touched, setTouched] = useState({
    name: false,
    manufacturer: false,
  });

  useEffect(() => {
    const fetchDevice = async () => {
      if (!id) return;
      
      setLoading(true);
      setError(null);
      
      try {
        const response = await apiClient.get(`/api/v1/devices/${id}`);
        const device: Device = response.data;
        setFormData({
          name: device.name,
          manufacturer: device.manufacturer,
        });
      } catch (err: any) {
        console.error('Error fetching device:', err);
        if (err.response?.data?.error?.message) {
          setError(err.response.data.error.message);
        } else {
          setError('デバイスの取得に失敗しました');
        }
        navigate('/devices');
      } finally {
        setLoading(false);
      }
    };

    fetchDevice();
  }, [id, navigate]);

  const handleChange = (field: keyof DeviceCreate) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [field]: event.target.value,
    }));
    setTouched((prev) => ({
      ...prev,
      [field]: true,
    }));
  };

  const validateForm = () => {
    const errors: Partial<Record<keyof DeviceCreate, string>> = {};
    
    if (!formData.name) {
      errors.name = '機器名は必須です';
    }
    if (!formData.manufacturer) {
      errors.manufacturer = 'メーカー名は必須です';
    }

    const pattern = /^[a-zA-Z0-9ぁ-んァ-ンー一-龥\s\-_.,&!@#()（）［］・、。]+$/;
    if (formData.name && !pattern.test(formData.name)) {
      errors.name = '使用できない文字が含まれています。使用可能な文字：日本語、英数字、記号（. , & ! @ # ( ) （ ） ［ ］ ・ 、 。 - _）';
    }
    if (formData.manufacturer && !pattern.test(formData.manufacturer)) {
      errors.manufacturer = '使用できない文字が含まれています。使用可能な文字：日本語、英数字、記号（. , & ! @ # ( ) （ ） ［ ］ ・ 、 。 - _）';
    }
    
    return errors;
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    setTouched({
      name: true,
      manufacturer: true,
    });

    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      if (id) {
        await apiClient.put(`/api/v1/devices/${id}`, formData);
        setSuccessMessage('機器を更新しました');
      } else {
        await apiClient.post('/api/v1/devices/', formData);
        setSuccessMessage('機器を登録しました');
      }
      setTimeout(() => {
        navigate('/devices');
      }, 2000);
    } catch (err: any) {
      console.error('Error saving device:', err);
      if (err.response?.data?.error?.message) {
        setError(err.response.data.error.message);
        
        if (err.response.data.error.details?.field === 'duplicate') {
          setTouched({
            name: true,
            manufacturer: true,
          });
        }
      } else {
        setError(id ? '機器の更新に失敗しました' : '機器の登録に失敗しました');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    const isFormDirty = touched.name || touched.manufacturer;
    if (isFormDirty) {
      setShowCancelDialog(true);
    } else {
      navigate('/devices');
    }
  };

  const errors = validateForm();

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" gutterBottom>
          {id ? '機器編集' : '機器登録'}
        </Typography>
      </Box>

      <Stack spacing={3} maxWidth="600px">
        <TextField
          label="機器名"
          value={formData.name}
          onChange={handleChange('name')}
          touched={touched.name}
          errorMessage={touched.name ? errors.name : undefined}
          required
          fullWidth
        />

        <TextField
          label="メーカー名"
          value={formData.manufacturer}
          onChange={handleChange('manufacturer')}
          touched={touched.manufacturer}
          errorMessage={touched.manufacturer ? errors.manufacturer : undefined}
          required
          fullWidth
        />

        <Box display="flex" gap={2}>
          <Button
            variant="text"
            onClick={handleCancel}
            disabled={loading}
          >
            キャンセル
          </Button>
          <Button
            type="submit"
            loading={loading}
            disabled={loading || Object.keys(errors).length > 0}
          >
            {id ? '更新' : '登録'}
          </Button>
        </Box>
      </Stack>

      <Dialog
        open={showCancelDialog}
        title="確認"
        confirmText="はい"
        cancelText="いいえ"
        onConfirm={() => navigate('/devices')}
        onCancel={() => setShowCancelDialog(false)}
      >
        <Typography>
          変更内容が保存されていません。
          <br />
          一覧画面に戻りますか？
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

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
}; 