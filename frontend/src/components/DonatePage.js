import React, { useState } from "react";
import "../styles/DonatePage.css";

const DonatePage = () => {
  const [customAmount, setCustomAmount] = useState("");

  return (
    <div className="donate-page">
      {/* Hero Section */}
      <div className="donate-hero">
        <h1 className="donate-title">Make a Difference Today</h1>
        <p className="donate-subtitle">
          Your support empowers individuals living with diabetes by funding essential resources, education, and medical assistance.
        </p>
      </div>

      {/* Donation Options */}
      <div className="donate-container">
        <div className="donate-card">
          <h2>Select a Donation Amount</h2>
          <div className="donate-options">
            <button className="donate-option">$10.00</button>
            <button className="donate-option">$25.00</button>
            <button className="donate-option">$50.00</button>
            <button className="donate-option">$100.00</button>
            <button className="donate-option">$250.00</button>
          </div>

          {/* Custom Amount */}
          <div className="custom-donate">
            <input
              type="number"
              placeholder="Enter custom amount"
              value={customAmount}
              onChange={(e) => setCustomAmount(e.target.value)}
            />
            <span className="currency">$</span>
          </div>

          {/* Donate Now Button */}
          <button className="donate-button">Donate Now</button>

          {/* Secure Message */}
          <p className="secure-message">🔒 Secure Payment Processing</p>
        </div>
      </div>

      {/* Why Donate Section */}
      <div className="why-donate">
        <h2>Why Your Donation Matters</h2>
        <p>Every dollar goes toward research, advocacy, and direct support for those affected by diabetes. Here’s how your contributions help:</p>
        <ul>
          <li>🩸 $25 - Provides a free glucose monitoring kit for a child in need</li>
          <li>📚 $50 - Funds educational materials for newly diagnosed individuals</li>
          <li>🩺 $100 - Supports a diabetes prevention workshop</li>
          <li>💙 $250 - Helps cover medical expenses for low-income families</li>
        </ul>
      </div>
    </div>
  );
};

export default DonatePage;
