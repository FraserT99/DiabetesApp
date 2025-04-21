import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/RegisterPage.css';

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
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  // Validation Rules 
  const validateName = (name) => /^[A-Za-z]{2,50}$/.test(name);
  const validatePassword = (password) =>
    /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$/.test(password);
  const validateEmail = (email) =>
    /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/.test(email);
  const validatePhone = (phone) =>
    /^\+?\d{10,15}$/.test(phone);
  const validateAge = (age) =>
    Number.isInteger(Number(age)) && age >= 18 && age <= 120;

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!firstName || !lastName || !email || !password || !age || !gender || !ethnicity || !diagnosis || !phone) {
      setError('Please fill in all required fields.');
      return;
    }

    if (!validateName(firstName)) {
      setError('First name must contain only letters (2–50 characters).');
      return;
    }

    if (!validateName(lastName)) {
      setError('Last name must contain only letters (2–50 characters).');
      return;
    }

    if (!validatePassword(password)) {
      setError('Password must be 8–20 characters and contain at least one letter and one number.');
      return;
    }

    if (!validateEmail(email)) {
      setError('Invalid email format.');
      return;
    }

    if (!validatePhone(phone)) {
      setError('Phone number must be 10–15 digits and may start with +.');
      return;
    }

    if (!validateAge(age)) {
      setError('Please enter a valid age between 18 and 120.');
      return;
    }

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
        family_history_diabetes: familyHistoryDiabetes,
        email,
        phone_number: phone
      });

      if (response.data.success) {
        setSuccess('Registration successful! Redirecting to login...');
        setError('');

        //Clear form
        setPassword('');
        setFirstName('');
        setLastName('');
        setAge('');
        setGender('');
        setEthnicity('');
        setDiagnosis('');
        setSmoking(false);
        setFamilyHistoryDiabetes(false);
        setEmail('');
        setPhone('');

        //Redirect after delay
        setTimeout(() => {
          setSuccess('');
          navigate('/login');
        }, 1500);
      } else {
        setError(response.data.message || 'Registration failed.');
        setSuccess('');
      }
    } catch (err) {
      const msg = err?.response?.data?.message || 'Something went wrong during registration.';
      setError(msg);
      setSuccess('');
    }
  };

  return (
    <main className="register-page">
      <div className="register-container">
        <h2>Register an account</h2>
        <form onSubmit={handleRegister} className="register-form">
          <div className="form-grid">
            <div className="form-group">
              <label>First Name</label>
              <input value={firstName} onChange={(e) => setFirstName(e.target.value)} placeholder="Enter your first name" />
            </div>

            <div className="form-group">
              <label>Last Name</label>
              <input value={lastName} onChange={(e) => setLastName(e.target.value)} placeholder="Enter your last name" />
            </div>

            <div className="form-group">
              <label>Password</label>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Enter your password" />
            </div>

            <div className="form-group">
              <label>Email Address</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Enter your email" />
            </div>

            <div className="form-group">
              <label>Phone Number</label>
              <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="Enter your phone number" />
            </div>

            <div className="form-group">
              <label>Age</label>
              <input type="number" value={age} onChange={(e) => setAge(e.target.value)} placeholder="Enter your age" />
            </div>

            <div className="form-group">
              <label>Gender</label>
              <select value={gender} onChange={(e) => setGender(e.target.value)}>
                <option value="">Select Gender</option>
                <option value="0">Male</option>
                <option value="1">Female</option>
              </select>
            </div>

            <div className="form-group">
              <label>Ethnicity</label>
              <select value={ethnicity} onChange={(e) => setEthnicity(e.target.value)}>
                <option value="">Select Ethnicity</option>
                <option value="0">Caucasian</option>
                <option value="1">African American</option>
                <option value="2">Asian</option>
                <option value="3">Other</option>
              </select>
            </div>

            <div className="form-group">
              <label>Diagnosis</label>
              <select value={diagnosis} onChange={(e) => setDiagnosis(e.target.value)}>
                <option value="">Select Diagnosis</option>
                <option value="1">Diabetic</option>
                <option value="0">Non-Diabetic</option>
              </select>
            </div>

            <div className="form-checkbox">
              <input type="checkbox" id="smoking" checked={smoking} onChange={(e) => setSmoking(e.target.checked)} />
              <label htmlFor="smoking">Do you smoke?</label>
            </div>

            <div className="form-checkbox">
              <input type="checkbox" id="familyHistoryDiabetes" checked={familyHistoryDiabetes} onChange={(e) => setFamilyHistoryDiabetes(e.target.checked)} />
              <label htmlFor="familyHistoryDiabetes">Family history of diabetes?</label>
            </div>
          </div>

          <div className="form-submit">
            <button type="submit">Register</button>
          </div>

          {error && <p className="error">{error}</p>}
          {success && <p className="success">{success}</p>}
        </form>
      </div>
    </main>
  );
};

export default RegisterPage;
