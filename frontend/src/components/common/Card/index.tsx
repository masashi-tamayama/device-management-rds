import {
  Card as MuiCard,
  CardHeader,
  CardContent,
  Alert,
} from '@mui/material';
import { LoadingSpinner } from '../LoadingSpinner';
import { CardProps } from './types';

export const Card = ({
  children,
  title,
  subtitle,
  headerAction,
  loading = false,
  error,
  ...props
}: CardProps) => {
  return (
    <MuiCard
      {...props}
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        ...props.sx,
      }}
    >
      {title && (
        <CardHeader
          title={title}
          subheader={subtitle}
          action={headerAction}
        />
      )}
      <CardContent sx={{ flexGrow: 1, position: 'relative' }}>
        {loading ? (
          <LoadingSpinner />
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          children
        )}
      </CardContent>
    </MuiCard>
  );
}; 