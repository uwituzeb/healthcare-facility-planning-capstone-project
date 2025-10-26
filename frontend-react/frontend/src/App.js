import logo from './logo.svg';
import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";
import LandingPage from './components/landingPage/landingPage';
import SignUpPage from './components/SignupPage/signupPage';
import LoginPage from './components/loginPage/loginPage';
import DashboardOverview from './components/dashboards/dashboardOverview';
import InteractiveMap from './components/interactiveMap';
import Recommendations from './components/recommendations';
import Reports from './components/reports';
import AccessibilityAnalysis from './components/accessibilityAnalysis';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<LandingPage />} />
        <Route path='*' element={<Navigate to='/' replace />} />
        <Route path='/signup' element={<SignUpPage />} />
        <Route path='/login' element={<LoginPage />} />
        <Route path='/dashboard/overview' element={<DashboardOverview/>} />
        <Route path='/dashboard/analysis' element={<AccessibilityAnalysis/>} />
        <Route path='/dashboard/map' element={<InteractiveMap/>} />
        <Route path='/dashboard/recommendations' element={<Recommendations/>} />
        <Route path='/dashboard/report' element={<Reports/>} />

      </Routes>
    </Router>
  );
}

export default App;
