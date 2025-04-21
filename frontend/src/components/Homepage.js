import React from 'react';
import { Link } from 'react-router-dom'; 
import '../styles/Homepage.css';

const Homepage = () => {
  return (
    <main>
      <section className="homepage-container">
        {/* First Box: Main Content */}
        <div className="box">
          <h3>MONITOR YOUR HEALTH</h3>
          <p>Track your blood sugar levels and manage your diabetes more effectively.</p>
          <Link to="/dashboard">
            <button>View Your Dashboard</button>
          </Link>
        </div>

        {/* Second Box: About Section */}
        <div className="box" id="about">
          <h3>ABOUT</h3>
          <p>Learn more about diabetes management and how this app can help you.</p>
          <Link to="/about">
            <button>About GlucoTrack</button>
          </Link>
        </div>

        {/* Third Box: FAQs Section */}
        <div className="box" id="faq">
          <h3>FAQS</h3>
          <p>Find answers to the most frequently asked questions about managing diabetes.</p>
          <Link to="/faq">
            <button>Frequently Asked Questions</button>
          </Link>
        </div>

        {/* Fourth Box: Resources Section */}
        <div className="box" id="resources">
          <h3>RESOURCES</h3>
          <p>Discover helpful resources for managing diabetes, including links to health organizations, support groups, and tools.</p>
          <Link to="/resources">
            <button>Explore Resources</button>
          </Link>
        </div>

        {/* Fifth Box: Register Section */}
        <div className="box" id="register">
          <h3>REGISTER</h3>
          <p>Sign up to get started on managing your diabetes effectively with GlucoTrack.</p>
          <Link to="/register">
            <button>Register Now</button>
          </Link>
        </div>

        {/* Sixth Box: Donate Section */}
        <div className="box" id="donate">
          <h3>DONATE</h3>
          <p>By contributing, you help provide resources, support, and education to individuals and families affected by this diabetes.</p>
          <Link to="/donate">
            <button>Donate</button>
          </Link>
        </div>
      </section>
    </main>
  );
};

export default Homepage;
