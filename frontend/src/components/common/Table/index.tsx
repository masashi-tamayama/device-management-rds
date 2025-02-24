import {
  Table as MuiTable,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Alert,
} from '@mui/material';
import { LoadingSpinner } from '../LoadingSpinner';
import { TableProps, Column } from './types';

export const Table = <T extends object>({
  columns,
  rows,
  loading = false,
  error,
  onRowClick,
  getRowId = (row: T) => (row as any).id,
  ...props
}: TableProps<T>) => {
  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <TableContainer component={Paper}>
      <MuiTable {...props}>
        <TableHead>
          <TableRow>
            {columns.map((column) => (
              <TableCell
                key={String(column.field)}
                style={{ width: column.width }}
              >
                {column.headerName}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={getRowId(row)}
              hover={!!onRowClick}
              onClick={() => onRowClick?.(row)}
              sx={{ cursor: onRowClick ? 'pointer' : 'default' }}
            >
              {columns.map((column) => (
                <TableCell key={String(column.field)}>
                  {column.renderCell
                    ? column.renderCell(row)
                    : row[column.field]?.toString()}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </MuiTable>
    </TableContainer>
  );
}; 