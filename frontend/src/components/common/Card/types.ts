import { CardProps as MuiCardProps } from '@mui/material';
import { ReactNode } from 'react';

export interface CardProps extends MuiCardProps {
  title?: string;
  subtitle?: string;
  headerAction?: ReactNode;
  loading?: boolean;
  error?: string;
} 