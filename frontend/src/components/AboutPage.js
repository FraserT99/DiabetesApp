import React from 'react';
import '../styles/AboutPage.css';

const AboutPage = () => {
  return (
    <main className="about-page">
      <div className="about-container">
        <div className="about-header">
          <h1>What is GlucoTrack?</h1>
          <p className="about-intro">
            GlucoTrack is a modern app helping individuals with diabetes manage their health with confidence. 
            Track blood sugar levels, monitor physical activity, maintain a healthy diet, and access expert 
            resources—all in one place.
          </p>
        </div>

        <section className="about-section">
          <h2>🎯 Our Mission</h2>
          <p>
            To help people living with diabetes lead a healthier, more fulfilling life through real-time insights, 
            personalised health plans, and supportive community features.
          </p>
        </section>

        <section className="about-features-why">
          <div className="features-column">
            <h3>⭐ Key Features</h3>
            <ul>
              <li>📊 Real-time blood sugar level tracking.</li>
              <li>🚶‍♂️ Monitor physical activity and calorie burn.</li>
              <li>📚 Access expert articles and diabetes tips.</li>
              <li>🎯 Set and track daily wellness goals.</li>
            </ul>
          </div>

          <div className="why-column">
            <h3>💡 Why Choose GlucoTrack?</h3>
            <ul>
              <li>🧠 Simple, intuitive interface for all users.</li>
              <li>📈 Personalised health dashboards and insights.</li>
              <li>⏱️ Stay updated with real-time progress reports.</li>
              <li>🔄 Continuous updates with new features.</li>
            </ul>
          </div>
        </section>
      </div>
    </main>
  );
};

export default AboutPage;
