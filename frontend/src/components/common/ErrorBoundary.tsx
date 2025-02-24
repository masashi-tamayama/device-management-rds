import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Box, Typography, Button } from '@mui/material';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('エラー詳細:', error, errorInfo);
  }

  private handleReload = () => {
    window.location.reload();
  };

  public render() {
    if (this.state.hasError) {
      return (
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          minHeight="60vh"
          gap={2}
        >
          <Typography variant="h4" color="error">
            エラーが発生しました
          </Typography>
          <Typography variant="body1" color="textSecondary">
            申し訳ありません。予期せぬエラーが発生しました。
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={this.handleReload}
          >
            ページを再読み込み
          </Button>
        </Box>
      );
    }

    return this.props.children;
  }
} 