import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import '../styles/RegisterPage.css'; // Import the styles for this page

const RegisterPage = () => {
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');
  const [ethnicity, setEthnicity] = useState('');
  const [diagnosis, setDiagnosis] = useState('');
  const [smoking, setSmoking] = useState(false);
  const [familyHistoryDiabetes, setFamilyHistoryDiabetes] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate(); // Using useNavigate to handle navigation

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/register', {
        password,
        first_name: firstName,
        last_name: lastName,
        age,
        gender,
        ethnicity,
        diagnosis,
        smoking,
        family_history_diabetes: familyHistoryDiabetes
      });

      if (response.data.success) {
        // Handle successful registration
        setSuccess(response.data.message);
        setError('');
        // Optionally, clear the input fields
        setPassword('');
        setFirstName('');
        setLastName('');
        setAge('');
        setGender('');
        setEthnicity('');
        setDiagnosis('');
        setSmoking(false);
        setFamilyHistoryDiabetes(false);
        
        // Redirect to login page or homepage (adjust the path as needed)
        setTimeout(() => {
          navigate('/login'); // Redirect to login page after registration
        }, 2000); // Redirect after 2 seconds
      } else {
        setError(response.data.message);
        setSuccess('');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
      setSuccess('');
    }
  };

  return (
    <main className="register-page">
      <div className="register-container">
        <h2>Register</h2>
        <form onSubmit={handleRegister}>
          <div className="form-group">
            <label htmlFor="firstName">First Name</label>
            <input
              type="text"
              id="firstName"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
              placeholder="Enter your first name"
            />
          </div>
          <div className="form-group">
            <label htmlFor="lastName">Last Name</label>
            <input
              type="text"
              id="lastName"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
              placeholder="Enter your last name"
            />
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
          </div>
          {/* Additional Fields for Patient Information */}
          <div className="form-group">
            <label htmlFor="age">Age</label>
            <input
              type="number"
              id="age"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              required
              placeholder="Enter your age"
            />
          </div>
          <div className="form-group">
            <label htmlFor="gender">Gender</label>
            <select
              id="gender"
              value={gender}
              onChange={(e) => setGender(e.target.value)}
              required
            >
              <option value="">Select Gender</option>
              <option value="0">Male</option>
              <option value="1">Female</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="ethnicity">Ethnicity</label>
            <select
              id="ethnicity"
              value={ethnicity}
              onChange={(e) => setEthnicity(e.target.value)}
              required
            >
              <option value="">Select Ethnicity</option>
              <option value="0">Caucasian</option>
              <option value="1">African American</option>
              <option value="2">Asian</option>
              <option value="3">Other</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="diagnosis">Diagnosis</label>
            <select
              id="diagnosis"
              value={diagnosis}
              onChange={(e) => setDiagnosis(e.target.value)}
              required
            >
              <option value="">Select Diagnosis</option>
              <option value="1">Diabetic</option>
              <option value="0">Non-Diabetic</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="smoking">Smoking</label>
            <input
              type="checkbox"
              id="smoking"
              checked={smoking}
              onChange={(e) => setSmoking(e.target.checked)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="familyHistoryDiabetes">Family History of Diabetes</label>
            <input
              type="checkbox"
              id="familyHistoryDiabetes"
              checked={familyHistoryDiabetes}
              onChange={(e) => setFamilyHistoryDiabetes(e.target.checked)}
            />
          </div>

          <button type="submit" className="register-btn">Register</button>
        </form>

        {/* Display success or error message */}
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
      </div>
    </main>
  );
};

export default RegisterPage;
