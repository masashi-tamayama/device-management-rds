import { createBrowserRouter } from 'react-router-dom';
import { Layout } from '../components/layout/Layout';
import { NotFound } from '../pages/error/NotFound';
import { DeviceList } from '../pages/devices/DeviceList';
import { DeviceDetail } from '../pages/devices/DeviceDetail';
import { DeviceForm } from '../pages/devices/DeviceForm';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    errorElement: <NotFound />,
    children: [
      {
        path: '/',
        element: <DeviceList />,
      },
      {
        path: '/devices',
        element: <DeviceList />,
      },
      {
        path: '/devices/:id',
        element: <DeviceDetail />,
      },
      {
        path: '/devices/new',
        element: <DeviceForm />,
      },
      {
        path: '/devices/:id/edit',
        element: <DeviceForm />,
      },
    ],
  },
]); 