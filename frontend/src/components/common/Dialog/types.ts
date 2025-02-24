import { DialogProps as MuiDialogProps } from '@mui/material';
import { ReactNode } from 'react';

export interface DialogProps extends Omit<MuiDialogProps, 'title'> {
  title: string;
  confirmText?: string;
  cancelText?: string;
  onConfirm?: () => void;
  onCancel?: () => void;
  loading?: boolean;
  confirmDisabled?: boolean;
  confirmVariant?: 'primary' | 'secondary' | 'danger';
  children: ReactNode;
} 