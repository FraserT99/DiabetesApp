import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/user');
        if (response.data.success) {
          setUserData(response.data.user);
        } else {
          navigate('/login');
        }
      } catch (err) {
        navigate('/login');
      }
    };

    fetchUserData();
  }, [navigate]);

  if (!userData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Welcome, {userData.username}</h2>
      <p>Your Health Stats:</p>
      {/* Example of user data */}
      <p>Blood Glucose Level: {userData.glucoseLevel}</p>
      <p>Last Update: {userData.lastUpdate}</p>
      {/* Add more health data as needed */}
    </div>
  );
}

export default Dashboard;
