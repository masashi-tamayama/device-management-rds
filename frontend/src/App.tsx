import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { DeviceList } from './components/DeviceList/DeviceList';
import { DeviceForm } from './components/DeviceForm/DeviceForm';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Navigate to="/devices" replace />} />
          <Route path="/devices" element={<DeviceList />} />
          <Route path="/devices/create" element={<DeviceForm />} />
          <Route path="/devices/edit/:id" element={<DeviceForm />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;