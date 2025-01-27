import React, { useState, useEffect } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Homepage from './components/Homepage';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import Navigation from './components/Navigation';
import AboutPage from './components/AboutPage';  // Import AboutPage
import DashboardPage from './components/DashboardPage';  // Import DashboardPage
import FAQPage from './components/FAQPage';  // Import FAQPage
import ResourcesPage from './components/ResourcesPage';  // Import ResourcesPage
import DonatePage from './components/DonatePage';  // Import DonatePage
import ProfilePage from './components/ProfilePage';  // Import DonatePage
import RewardsPage from './components/RewardsPage';  // Import DonatePage
import LeaderboardPage from './components/LeaderboardPage';  // Import DonatePage


const App = () => {
  // Lift the username state to App.js
  const [username, setUsername] = useState(null);

  // Effect to check localStorage for the username when the component mounts
  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setUsername(storedUsername); // Set the username state from localStorage
    }
  }, []); // Runs once when the component mounts

  return (
    <div className="app-container">
      <Router>
        <Navigation username={username} setUsername={setUsername} /> {/* Pass username and setUsername as props */}
        <main>
          <Routes>
            <Route path="/" element={<Homepage />} />
            <Route path="/login" element={<LoginPage setUsername={setUsername} />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/faq" element={<FAQPage />} />
            <Route path="/resources" element={<ResourcesPage />} />
            <Route path="/donate" element={<DonatePage />} />
            <Route path="/profile" element={<ProfilePage />} /> {/* Add Profile Route */}
            <Route path="/rewards" element={<RewardsPage />} /> {/* Add Rewards Route */}
            <Route path="/leaderboard" element={<LeaderboardPage />} /> {/* Add Leaderboards Route */}
          </Routes>
        </main>
        <footer>
          <p>&copy; 2024 Diabetes Management App - Developed by Fraser Thomson</p>
        </footer>
      </Router>
    </div>
  );
};

export default App;
