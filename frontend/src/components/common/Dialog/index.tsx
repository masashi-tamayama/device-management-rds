import {
  Dialog as MuiDialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Button } from '../Button';
import { DialogProps } from './types';

export const Dialog = ({
  title,
  children,
  confirmText = '確認',
  cancelText = 'キャンセル',
  onConfirm,
  onCancel,
  loading = false,
  confirmDisabled = false,
  confirmVariant = 'primary',
  ...props
}: DialogProps) => {
  return (
    <MuiDialog
      {...props}
      onClose={(event, reason) => {
        if (loading) return;
        if (props.onClose) {
          props.onClose(event, reason);
        }
      }}
    >
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>{children}</DialogContent>
      <DialogActions>
        {onCancel && (
          <Button
            variant="text"
            onClick={onCancel}
            disabled={loading}
          >
            {cancelText}
          </Button>
        )}
        {onConfirm && (
          <Button
            variant={confirmVariant}
            onClick={onConfirm}
            loading={loading}
            disabled={confirmDisabled}
          >
            {confirmText}
          </Button>
        )}
      </DialogActions>
    </MuiDialog>
  );
}; 