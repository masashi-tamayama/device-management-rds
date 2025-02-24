import { useState } from 'react';
import { Box, Typography, Stack, Alert, Snackbar } from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import { TextField } from '../../components/common/TextField';
import { Button } from '../../components/common/Button';
import { DeviceCreate } from '../../types/device';
import apiClient from '../../api/client';

export const DeviceForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [formData, setFormData] = useState<DeviceCreate>({
    name: '',
    manufacturer: '',
  });
  const [touched, setTouched] = useState({
    name: false,
    manufacturer: false,
  });

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
    
    return errors;
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    // 全てのフィールドをタッチ済みにする
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
      await apiClient.post('/api/v1/devices/', formData);
      setSuccessMessage('機器を登録しました');
      setTimeout(() => {
        navigate('/devices');
      }, 2000);
    } catch (err) {
      console.error('Error creating device:', err);
      setError('機器の登録に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const errors = validateForm();

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" gutterBottom>
          機器登録
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
            onClick={() => navigate('/devices')}
            disabled={loading}
          >
            キャンセル
          </Button>
          <Button
            type="submit"
            loading={loading}
            disabled={loading || Object.keys(errors).length > 0}
          >
            登録
          </Button>
        </Box>
      </Stack>

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