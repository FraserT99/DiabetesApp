import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "../styles/DashboardPage.css"; 

const DashboardPage = () => {
  const [username, setUsername] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (!storedUsername) {
      navigate('/login'); //Redirect if not logged in
    } else {
      setUsername(storedUsername);
    }
  }, [navigate]);

  if (!username) {
    return null; //Prevent rendering until username is set
  }

  return (
    <div className="dashboard-page">
      {/* Pass username in the iframe URL */}
      <iframe
        src={`http://localhost:5000/dashboard?username=${username}`}
        title="Diabetes Health Dashboard"
        sandbox="allow-scripts allow-same-origin allow-forms"
      />
    </div>
  );
};

export default DashboardPage;
