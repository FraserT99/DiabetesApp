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
    {
      question: "Can I set reminders for my medications?",
      answer: "Yes, GlucoTrack allows you to set custom reminders for your medications to help you stay on track with your treatment plan.",
    },
    {
      question: "Is there a community within GlucoTrack?",
      answer: "Yes, GlucoTrack offers a supportive community where users can connect with others managing their diabetes, share experiences, and offer support.",
    },
    {
      question: "How do I update my profile information?",
      answer: "You can easily update your profile information by going to the settings section of the app and editing your personal details.",
    },
    {
      question: "Does GlucoTrack provide personalized diet recommendations?",
      answer: "Yes, GlucoTrack provides personalized diet recommendations based on your health data and goals to help you maintain a balanced diet.",
    },
  ];

  return (
    <div className="faq-page">
      <div className="faq-container">
        <h1 className="faq-title">Frequently Asked Questions</h1>
        <div className="faq-list">
          {faqData.map((faq, index) => (
            <div
              className={`faq-item ${openIndex === index ? 'open' : ''}`}
              key={index}
            >
              <div
                className="faq-question-container"
                onClick={() => toggleAnswer(index)}
              >
                <h2 className="faq-question">{faq.question}</h2>
                <span
                  className={`faq-icon ${openIndex === index ? 'open' : ''}`}
                ></span>
              </div>
              <div className="faq-answer">{faq.answer}</div>
            </div>
          ))}
        </div>

        {/* New section below FAQ list with a heading, paragraph, and the Contact Us button */}
        <section className="faq-footer">
          <h2>Need More Information?</h2>
          <p>
            If you have additional questions or need further assistance, don't hesitate to reach out to our support team. We're here to help you navigate the GlucoTrack app and ensure that you're getting the most out of your diabetes management journey.
          </p>
          <div className="contact-btn-container">
            <button className="contact-btn">
              Contact Us
            </button>
          </div>
        </section>
      </div>
    </div>
  );
};

export default FAQPage;
