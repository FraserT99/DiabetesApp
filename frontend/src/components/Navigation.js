import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Using Link for navigation

const Navigation = ({ username, setUsername }) => {
  const navigate = useNavigate(); // For programmatic navigation

  // Initialize username from localStorage when the component mounts
  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setUsername(storedUsername);  // Set the username if present in localStorage
    }
  }, [setUsername]);

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('username'); // Remove username from localStorage
    setUsername(null); // Clear the username state
    navigate('/login'); // Redirect to the login page
  };

  return (
    <header>
      {/* Container for the Logo and Title */}
      <div className="logo-title-container">
        <img src="/logo.png" alt="Logo" className="logo" />
        <h1 className="title">GlucoTrack</h1>
      </div>

      {/* Display username if the user is logged in */}
      {username && (
        <div className="username-display">
          Logged in as: {username}
        </div>
      )}

      {/* Navigation links */}
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/about">About</Link>
          </li>
          <li>
            <Link to="/faq">FAQs</Link>
          </li>
          <li>
            <Link to="/resources">Resources</Link>
          </li>
          <li>
            <Link to="/donate">Donate</Link>
          </li>

          {/* Show these links only if the user is logged in */}
          {username && (
            <>
              <li>
                <Link to="/dashboard">Dashboard</Link>
              </li>
              <li>
                <Link to="/leaderboard">Leaderboards</Link>
              </li>
              <li>
                <Link to="/rewards">Rewards</Link>
              </li>
              <li>
                <Link to="/profile">Profile</Link>
              </li>
            </>
          )}

          {/* Show Register and Login links if the user is not logged in */}
          {!username && (
            <>
              <li>
                <Link to="/register">Register</Link>
              </li>
              <li>
                <Link to="/login">Login</Link>
              </li>
            </>
          )}

          {/* Logout button if logged in */}
          {username && (
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          )}
        </ul>
      </nav>
    </header>
  );
};

export default Navigation;
