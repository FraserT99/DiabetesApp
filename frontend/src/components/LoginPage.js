import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/LoginPage.css';

const LoginPage = ({ setUsername }) => {
  const [username, setUsernameState] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const trimmedUsername = username.trim();
    const trimmedPassword = password.trim();

    if (trimmedUsername.length < 3 || trimmedPassword.length < 6) {
      setError('Username or password is too short.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/login', {
        username: trimmedUsername,
        password: trimmedPassword
      });

      if (response.data.success) {
        setSuccess('Login successful! Redirecting...');
        localStorage.setItem('username', response.data.username);
        setUsername(response.data.username);

        setTimeout(() => {
          setSuccess('');
          navigate('/');
        }, 1000);
      } else {
        setError(response.data.message || 'Login failed.');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
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
              onChange={(e) => setUsernameState(e.target.value)}
              required
              placeholder="Enter your username"
            />
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
            <div className="forgot-links">
              <a href="/forgot-password" className="forgot-link">Forgot your password?</a>
            </div>
          </div>

          <button type="submit" className="login_button">Login</button>
        </form>

        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
      </div>
    </main>
  );
};

export default LoginPage;
