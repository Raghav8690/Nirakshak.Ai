import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import DashboardPage from './pages/DashboardPage';
import EngagementPage from './pages/EngagementPage';
import ExplainabilityPage from './pages/ExplainabilityPage';
import AdminPage from './pages/AdminPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardPage />} />
          <Route path="engagement" element={<EngagementPage />} />
          <Route path="explainability" element={<ExplainabilityPage />} />
          <Route path="analytics" element={<AdminPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
