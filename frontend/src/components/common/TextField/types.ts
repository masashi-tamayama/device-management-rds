import { StandardTextFieldProps } from '@mui/material';

export interface TextFieldProps extends StandardTextFieldProps {
  loading?: boolean;
  touched?: boolean;
  errorMessage?: string;
} 