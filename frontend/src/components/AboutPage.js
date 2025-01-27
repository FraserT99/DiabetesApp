import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/AboutPage.css';

const AboutPage = () => {
  return (
    <main className="about-page">
      <div className="about-container">
        
        <section className="about-header">
          <h1>Welcome to GlucoTrack</h1>
          <p>Your personal health companion for managing diabetes.</p>
        </section>

        <section className="about-content">
          <div className="about-text">
            <h2>What is GlucoTrack?</h2>
            <p>
              GlucoTrack is an innovative app designed to assist individuals with diabetes in managing their condition with ease and precision. It offers a user-friendly interface to track blood sugar levels, monitor physical activity, maintain a healthy diet, and gain access to personalized educational resources—all in one place. Whether you're a diabetic patient, a caregiver, or a health-conscious individual, GlucoTrack provides essential tools to stay in control of your health.
            </p>

            <h3>Our Mission</h3>
            <p>
              Our mission at GlucoTrack is to provide individuals living with diabetes the ability to lead a healthier, more fulfilling life. We aim to help you feel empowered and informed by offering real-time data insights, personalized health plans, and community support, enabling better decision-making in managing your condition.
            </p>

            <h3>Key Features</h3>
            <ul>
              <li>Track blood sugar levels effortlessly with real-time readings.</li>
              <li>Monitor physical activity, steps, and daily calorie burn to stay active.</li>
              <li>Access a library of expert articles, tips, and diabetes management resources.</li>
              <li>Set daily goals for diet, exercise, and blood sugar control.</li>
            </ul>

            <h3>Why Choose GlucoTrack?</h3>
            <p>
              Managing diabetes can be overwhelming at times, but with GlucoTrack, you don’t have to do it alone. Our app gives you the tools, support, and motivation to make healthier choices every day. Here’s why you should choose GlucoTrack:
            </p>
            <ul>
              <li>Intuitive and easy-to-use interface for all users, no tech skills required.</li>
              <li>Personalized health tracking, from blood glucose to activity levels.</li>
              <li>Real-time insights and progress reports that help you make informed decisions.</li>
              <li>Regular updates with the latest information and features tailored to your health journey.</li>
            </ul>

            <div className="cta-container">
              <Link to="/register" className="cta-btn">Get Started</Link>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
};

export default AboutPage;
