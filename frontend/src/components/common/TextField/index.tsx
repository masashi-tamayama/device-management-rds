import { TextField as MuiTextField, CircularProgress } from '@mui/material';
import { TextFieldProps } from './types';

export const TextField = ({
  loading = false,
  touched = false,
  errorMessage,
  helperText,
  disabled,
  ...props
}: TextFieldProps) => {
  const hasError = touched && Boolean(errorMessage);

  return (
    <MuiTextField
      {...props}
      error={hasError}
      helperText={hasError ? errorMessage : helperText}
      disabled={disabled || loading}
      InputProps={{
        ...props.InputProps,
        endAdornment: loading ? (
          <CircularProgress size={20} />
        ) : (
          props.InputProps?.endAdornment
        ),
      }}
    />
  );
}; 