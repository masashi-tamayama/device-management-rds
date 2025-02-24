import { TableProps as MuiTableProps } from '@mui/material';
import { ReactNode } from 'react';

export interface Column<T> {
  field: keyof T;
  headerName: string;
  width?: number;
  renderCell?: (row: T) => ReactNode;
}

export interface TableProps<T> extends Omit<MuiTableProps, 'rows'> {
  columns: Column<T>[];
  rows: T[];
  loading?: boolean;
  error?: string;
  onRowClick?: (row: T) => void;
  getRowId?: (row: T) => string;
} 