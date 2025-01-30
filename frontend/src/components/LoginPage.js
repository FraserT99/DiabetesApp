import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';  // Import useNavigate for redirect
import '../styles/LoginPage.css'; // Import the styles for this page

const LoginPage = ({ setUsername }) => {
  const [username, setUsernameState] = useState(''); // Local state for username
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate(); // Initialize the navigate function

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/login', {
        username,
        password
      });

      if (response.data.success) {
        setSuccess(response.data.message); // Show success message
        setError('');
        localStorage.setItem('username', response.data.username); // Store username in localStorage
        setUsername(response.data.username); // Update global username state via props
        navigate('/');  // Redirect to homepage after login
      } else {
        setError(response.data.message); // Display error message
        setSuccess('');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
      setSuccess('');
    }
  };

  return (
    <main className="login-page">
      <div className="login-container">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsernameState(e.target.value)} // Update local state
              required
              placeholder="Enter your username"
            />
            {/* Forgot Username Link */}
            <div className="forgot-links">
              <a href="/forgot-username" className="forgot-link">Forgot your username?</a>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
            />
            {/* Forgot Password Link */}
            <div className="forgot-links">
              <a href="/forgot-password" className="forgot-link">Forgot your password?</a>
            </div>
          </div>

          <button type="submit" className="login-btn">Login</button>
        </form>

        {/* Error and Success Messages */}
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
      </div>
    </main>
  );
};

export default LoginPage;
