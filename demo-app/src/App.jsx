import { useState } from 'react';
import { Navigate, NavLink, Outlet, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard.jsx';
import Login from './pages/Login.jsx';
import Settings from './pages/Settings.jsx';

const demoAccount = {
  email: 'qa@example.test',
  password: 'demo-password',
};

function Workspace({ onLogout }) {
  return (
    <>
      <header className="workspace-header">
        <div className="workspace-bar">
          <div className="brand">
            <span className="brand-mark" aria-hidden="true" />
            <span>Agentic QA Tester</span>
          </div>
          <nav className="workspace-nav" aria-label="Workspace">
            <NavLink to="/dashboard" data-testid="dashboard-link">Dashboard</NavLink>
            <NavLink to="/settings" data-testid="settings-link">Settings</NavLink>
          </nav>
          <button
            className="button button-secondary"
            type="button"
            onClick={onLogout}
            data-testid="logout-button"
          >
            Logout
          </button>
        </div>
      </header>
      <Outlet />
    </>
  );
}

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const landingPath = isAuthenticated ? '/dashboard' : '/login';

  function login(email, password) {
    if (email !== demoAccount.email || password !== demoAccount.password) {
      return false;
    }

    setIsAuthenticated(true);
    return true;
  }

  return (
    <Routes>
      <Route
        path="/login"
        element={isAuthenticated
          ? <Navigate to="/dashboard" replace />
          : <Login account={demoAccount} onLogin={login} />}
      />
      <Route
        element={isAuthenticated
          ? <Workspace onLogout={() => setIsAuthenticated(false)} />
          : <Navigate to="/login" replace />}
      >
        <Route path="/dashboard" element={<Dashboard email={demoAccount.email} />} />
        <Route path="/settings" element={<Settings email={demoAccount.email} />} />
      </Route>
      <Route path="*" element={<Navigate to={landingPath} replace />} />
    </Routes>
  );
}
