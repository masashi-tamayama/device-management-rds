import { Box, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export const NotFound = () => {
  const navigate = useNavigate();

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="60vh"
      gap={2}
    >
      <Typography variant="h1" color="primary">
        404
      </Typography>
      <Typography variant="h5" color="textSecondary">
        ページが見つかりません
      </Typography>
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/')}
      >
        ホームに戻る
      </Button>
    </Box>
  );
}; 