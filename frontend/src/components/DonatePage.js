import React from 'react';
import '../styles/DonatePage.css';

const DonatePage = () => {
  return (
    <div className="donate-page">
      <div className="donate-container">
        <h1 className="donate-title">Support Our Cause</h1>
        <p className="donate-description">
          Your generous donations help us provide support, educational resources, and life-changing services for those affected by diabetes. Every contribution makes a real difference in the lives of many.
        </p>
        <div className="donate-action">
          <button className="donate-button">Donate Now</button>
        </div>
        <div className="donate-info">
          <p>Choose your donation amount below or enter a custom amount.</p>
          {/* Add additional donation options or an embedded form here */}
        </div>
      </div>
    </div>
  );
};

export default DonatePage;
