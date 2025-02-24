import { Button as MuiButton, CircularProgress } from '@mui/material';
import { ButtonProps } from './types';

export const Button = ({
  children,
  variant = 'primary',
  loading = false,
  disabled,
  fullWidth = false,
  ...props
}: ButtonProps) => {
  // variantに基づいてMUIのvariantとcolorを設定
  const getButtonProps = () => {
    switch (variant) {
      case 'primary':
        return { variant: 'contained' as const, color: 'primary' as const };
      case 'secondary':
        return { variant: 'contained' as const, color: 'secondary' as const };
      case 'danger':
        return { variant: 'contained' as const, color: 'error' as const };
      case 'text':
        return { variant: 'text' as const, color: 'primary' as const };
      default:
        return { variant: 'contained' as const, color: 'primary' as const };
    }
  };

  const { variant: muiVariant, color } = getButtonProps();

  return (
    <MuiButton
      {...props}
      variant={muiVariant}
      color={color}
      disabled={disabled || loading}
      fullWidth={fullWidth}
      sx={{
        position: 'relative',
        minWidth: '120px',
        ...props.sx,
      }}
    >
      {loading && (
        <CircularProgress
          size={24}
          sx={{
            position: 'absolute',
            color: 'inherit',
          }}
        />
      )}
      <span style={{ visibility: loading ? 'hidden' : 'visible' }}>
        {children}
      </span>
    </MuiButton>
  );
}; 