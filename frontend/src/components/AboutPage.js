import React from 'react';
import '../styles/AboutPage.css';

const AboutPage = () => {
  return (
    <main className="about-page">
      <div className="about-container">
        
        <section className="about-content">
          <div className="about-text">
            <h2>What is GlucoTrack?</h2>
            <p>
              GlucoTrack is a powerful app designed to assist individuals with diabetes in managing their condition effectively. Whether you are monitoring your blood sugar levels, tracking your daily steps, or accessing personalized educational resources, GlucoTrack makes it easier to stay on top of your health goals.
            </p>
            <h3>Our Mission</h3>
            <p>
              Our mission is to empower people with diabetes to live healthier, more confident lives by providing accessible tools and resources that help improve overall wellness.
            </p>
            <h3>Features</h3>
            <ul>
              <li>Track blood sugar levels effortlessly.</li>
              <li>Monitor physical activity and diet.</li>
              <li>Access educational resources and expert advice.</li>
              <li>Stay connected with a supportive community.</li>
            </ul>
            <div className="cta-container">
              <a href="/get-started" className="cta-btn">Get Started</a>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
};

export default AboutPage;
