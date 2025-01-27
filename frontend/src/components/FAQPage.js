import React, { useState } from 'react';
import '../styles/FAQPage.css'; // Add this file for custom styles

const FAQPage = () => {
  const [openIndex, setOpenIndex] = useState(null);

  const toggleAnswer = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  const faqData = [
    {
      question: "What is GlucoTrack?",
      answer: "GlucoTrack is a diabetes management app that helps individuals track their blood sugar levels, manage medications, and access educational resources.",
    },
    {
      question: "How do I track my blood sugar levels?",
      answer: "You can input your blood sugar readings manually or sync the app with compatible devices to track your levels automatically.",
    },
    {
      question: "How secure is my data?",
      answer: "We use the latest encryption techniques to ensure that your personal data and health information are secure.",
    },
    {
      question: "Can I share my data with my doctor?",
      answer: "Yes, you can share your health data with your healthcare provider directly through the app, making it easier for them to monitor your progress.",
    },
    {
      question: "Is GlucoTrack free to use?",
      answer: "Yes, GlucoTrack is free to download and use. However, some premium features may be available for a fee.",
    },
    {
      question: "How can I contact customer support?",
      answer: "You can reach out to customer support via the contact form on the app or by emailing support@glucotrack.com.",
    },
  ];

  return (
    <div className="faq-page">
      <div className="faq-container"> {/* New container around the title and FAQs */}
        <h1 className="faq-title">Frequently Asked Questions</h1>
        <div className="faq-list">
          {faqData.map((faq, index) => (
            <div className="faq-item" key={index}>
              <div
                className="faq-question-container"
                onClick={() => toggleAnswer(index)}
              >
                <h2 className="faq-question">{faq.question}</h2>
                <span
                  className={`faq-icon ${openIndex === index ? 'open' : ''}`}
                ></span>
              </div>
              {openIndex === index && <p className="faq-answer">{faq.answer}</p>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FAQPage;
