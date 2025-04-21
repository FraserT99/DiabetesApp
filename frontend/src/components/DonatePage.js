import React, { useState } from "react";
import "../styles/DonatePage.css";

const DonatePage = () => {
  const [customAmount, setCustomAmount] = useState("");

  return (
    <main className="donate-page">
      <div className="donate-content">
        {/* Left Column – Text & Info */}
        <div className="donate-info">
          <h1 className="donate-title">Make a Difference Today</h1>
          <p className="donate-subtitle">
            Your support empowers individuals living with diabetes by funding essential resources,
            education, and medical assistance. Every contribution goes directly toward building a healthier future.
          </p>

          {/* Line space */}
          <br />

          <p className="donate-subtitle">
            Whether it's helping a child monitor their blood glucose, providing educational tools to those newly diagnosed,
            or covering critical medical expenses—your donation creates real change.
          </p>

          <br />

          <div className="why-donate">
            <h2>Why Your Donation Matters</h2>
            <p>
              Every dollar goes toward research, advocacy, and direct support for those affected by diabetes.
              Here’s how your contributions help:
            </p>        
          <br />
            <ul>
              <li>🩸 <strong>$25</strong> - Provides a free glucose monitoring kit for a child in need</li>
              <li>📚 <strong>$50</strong> - Funds educational materials for newly diagnosed individuals</li>
              <li>🩺 <strong>$100</strong> - Supports a diabetes prevention workshop</li>
              <li>💙 <strong>$250</strong> - Helps cover medical expenses for low-income families</li>
            </ul>
          </div>
        </div>

        {/* Right Column – Donation Card */}
        <div className="donate-card">
          <h2>Select a Donation Amount</h2>

          <div className="donate-options-grid">
            <button className="donate-option">$10.00</button>
            <button className="donate-option">$100.00</button>
            <button className="donate-option">$25.00</button>
            <button className="donate-option">$250.00</button>
            <button className="donate-option">$50.00</button>
            <button className="donate-option">$500.00</button>
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

          <button className="donate-button">Donate Now</button>
          <p className="secure-message">🔒 Secure Payment Processing</p>
        </div>
      </div>
    </main>
  );
};

export default DonatePage;
