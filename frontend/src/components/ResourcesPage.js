import React from 'react';
import '../styles/ResourcesPage.css';

const ResourcesPage = () => {
  const resources = [
    {
      title: 'American Diabetes Association',
      url: 'https://www.diabetes.org/',
      description: 'Official website offering resources, educational materials, and support for individuals with diabetes.',
      icon: 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/ADA_logo.svg/1200px-ADA_logo.svg.png'
    },
    {
      title: 'CDC Diabetes Resources',
      url: 'https://www.cdc.gov/diabetes/',
      description: 'The CDC’s comprehensive guide to managing diabetes, including prevention and care strategies.',
      icon: 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/CDC_logo.svg/1200px-CDC_logo.svg.png'
    },
    {
      title: 'Diabetes.co.uk',
      url: 'https://www.diabetes.co.uk/',
      description: 'UK-based diabetes community offering support, educational resources, and an online diabetes management program.',
      icon: 'https://www.diabetes.co.uk/favicon.ico'
    },
    // Additional example resources
    {
      title: 'Example Resource 1',
      url: 'https://www.example.com/',
      description: 'This is an example resource. Replace this with actual resource information.',
      icon: 'https://via.placeholder.com/40'
    },
    {
      title: 'Example Resource 2',
      url: 'https://www.example2.com/',
      description: 'Another placeholder resource, useful for testing. Replace with real content.',
      icon: 'https://via.placeholder.com/40'
    },
    {
      title: 'Example Resource 3',
      url: 'https://www.example3.com/',
      description: 'An additional example. This is a placeholder and should be replaced later.',
      icon: 'https://via.placeholder.com/40'
    }
  ];

  return (
    <div className="resources-page">
      <div className="resources-container"> {/* New container wrapping the title and resource cards */}
        <h1 className="resources-title">Diabetes Resources</h1>
        <div className="resources-list">
          {resources.map((resource, index) => (
            <div className="resource-card" key={index}>
              <div className="resource-icon-container">
                <img className="resource-icon" src={resource.icon} alt={resource.title} />
              </div>
              <div className="resource-content">
                <h2 className="resource-title">{resource.title}</h2>
                <p className="resource-description">{resource.description}</p>
              </div>
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
    </div>
  );
};

export default ResourcesPage;
