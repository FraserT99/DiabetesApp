import React from 'react';
import '../styles/ResourcesPage.css';

const resources = {
  education: [
    {
      title: 'American Diabetes Association',
      url: 'https://www.diabetes.org/',
      description: 'Official website offering resources, educational materials, and support for individuals with diabetes.',
      icon: '/images/ADA.png'
    },
    {
      title: 'CDC Diabetes Resources',
      url: 'https://www.cdc.gov/diabetes/',
      description: 'The CDC’s comprehensive guide to managing diabetes, including prevention and care strategies.',
      icon: '/images/CDC.png'
    }
  ],
  support: [
    {
      title: 'Diabetes.co.uk',
      url: 'https://www.diabetes.co.uk/',
      description: 'UK-based diabetes community offering support, educational resources, and an online diabetes management program.',
      icon: '/images/DUK.png'
    },
    {
      title: 'Breakthrough T1D',
      url: 'https://www.breakthrought1d.org/',
      description: 'Leading global organisation funding Type 1 diabetes research, offering support and advocacy.',
      icon: '/images/Breakthrough.png'
    }
  ],
  tools: [
    {
      title: 'GlucoTrack App',
      url: 'http://localhost:3000/',
      description: 'A modern diabetes tracking app that helps users monitor blood glucose levels and manage their condition effectively.',
      icon: '/images/logo.png'
    },
    {
      title: 'MySugr App',
      url: 'https://www.mysugr.com/',
      description: 'A diabetes logbook app designed to simplify blood sugar tracking with smart insights and reminders.',
      icon: '/images/MySugr.png'
    }
  ]
};

const ResourcesPage = () => {
  const categoryPairs = [['education', 'support'], ['tools']];

  return (
    <div className="resources-page">
      <div className="resources-container">
        <h1 className="resources-title">Diabetes Resources</h1>
        <p className="resources-subtitle">Your Guide to Trusted Diabetes Information</p>
        <p className="resources-intro">
          We’ve curated a list of reliable resources to help you stay informed about diabetes management, treatment, and support communities.
        </p>

        {categoryPairs.map((pair, pairIndex) => (
          <div key={pairIndex}>
            <div className="category-row">
              {pair.map((category, i) => (
                <React.Fragment key={category}>
                  <div className="resource-category">
                    <h3 className="category-title">
                      {category.charAt(0).toUpperCase() + category.slice(1)} Resources
                    </h3>
                    <div className="resources-list">
                      {resources[category].map((resource, index) => (
                        <div className="resource-card" key={index}>
                          <img className="resource-icon" src={resource.icon} alt={resource.title} />
                          <h2 className="resource-title">{resource.title}</h2>
                          <p className="resource-description">{resource.description}</p>
                          <a
                            href={resource.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="resource-link"
                          >
                            Visit Website
                          </a>
                        </div>
                      ))}
                    </div>
                  </div>

                  {pair.length === 2 && i === 0 && <div className="category-separator"></div>}
                </React.Fragment>
              ))}
            </div>

            {pairIndex === 0 && <div className="horizontal-separator"></div>}
          </div>
        ))}

        <section className="resources-footer">
          <h2>Know a Great Resource?</h2>
          <p>If you have a valuable diabetes-related resource that should be featured here, let us know!</p>
          <button className="suggest-resource-btn">Suggest a Resource</button>
        </section>
      </div>
    </div>
  );
};

export default ResourcesPage;
