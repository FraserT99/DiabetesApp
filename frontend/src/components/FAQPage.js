import React, { useState } from 'react';
import '../styles/FAQPage.css';

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
      answer: "Yes, you can share your health data with your healthcare provider directly through the app.",
    },
    {
      question: "Is GlucoTrack free to use?",
      answer: "Yes, GlucoTrack is free to download and use. However, some premium features may be available for a fee.",
    },
    {
      question: "Can I set reminders for my medications?",
      answer: "Yes, GlucoTrack allows you to set custom reminders for your medications to help you stay on track.",
    },
    {
      question: "How do I update my profile information?",
      answer: "Go to the settings section of the app to edit your personal details easily.",
    },
    {
      question: "Does GlucoTrack provide personalized diet recommendations?",
      answer: "Yes, GlucoTrack provides personalized diet guidance based on your health data and goals.",
    }
  ];

  return (
    <main className="faq-page">
      <div className="faq-container">
        <h1 className="faq-title">Frequently Asked Questions</h1>

        <div className="faq-columns">
          <div className="faq-column">
            {faqData.slice(0, 4).map((faq, index) => (
              <div className="faq-box" key={index}>
                <h3 className="faq-question" onClick={() => toggleAnswer(index)}>
                  {faq.question}
                  <span className="faq-icon">{openIndex === index ? '▲' : '▼'}</span>
                </h3>
                {openIndex === index && <p className="faq-answer">{faq.answer}</p>}
              </div>
            ))}
          </div>

          <div className="faq-column">
            {faqData.slice(4).map((faq, index) => (
              <div className="faq-box" key={index + 4}>
                <h3 className="faq-question" onClick={() => toggleAnswer(index + 4)}>
                  {faq.question}
                  <span className="faq-icon">{openIndex === index + 4 ? '▲' : '▼'}</span>
                </h3>
                {openIndex === index + 4 && <p className="faq-answer">{faq.answer}</p>}
              </div>
            ))}
          </div>
        </div>

        <section className="faq-footer">
          <h2>Need More Information?</h2>
          <p>
            Have additional questions? Reach out to our support team — we're here to help you get the most from your GlucoTrack experience.
          </p>
          <div className="contact-btn-container">
            <button className="contact-btn">Contact Us</button>
          </div>
        </section>
      </div>
    </main>
  );
};

export default FAQPage;
