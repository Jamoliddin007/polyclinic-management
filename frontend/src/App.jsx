import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout.jsx';
import ProtectedRoute from './components/ProtectedRoute.jsx';
import Login from './pages/Login.jsx';
import Dashboard from './pages/Dashboard.jsx';
import PatientsList from './pages/PatientsList.jsx';
import PatientForm from './pages/PatientForm.jsx';
import DoctorsList from './pages/DoctorsList.jsx';
import VisitsList from './pages/VisitsList.jsx';
import VisitCreate from './pages/VisitCreate.jsx';
import VisitDetail from './pages/VisitDetail.jsx';

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard"          element={<Dashboard />} />
        <Route path="/patients"           element={<PatientsList />} />
        <Route path="/patients/new"       element={<PatientForm />} />
        <Route path="/patients/:id/edit"  element={<PatientForm />} />
        <Route path="/doctors"            element={<DoctorsList />} />
        <Route path="/visits"             element={<VisitsList />} />
        <Route path="/visits/new"         element={<VisitCreate />} />
        <Route path="/visits/:id"         element={<VisitDetail />} />
      </Route>

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
