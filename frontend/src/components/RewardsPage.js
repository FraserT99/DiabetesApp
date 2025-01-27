import React from 'react';
import '../styles/RewardsPage.css'; // Add this file for custom styles

const Rewards = () => {
  const rewardsData = [
    { id: 1, title: '10% Off Voucher', points: 500, imgSrc: '/images/voucher.png' },
    { id: 2, title: 'Profile Badges', points: 100, imgSrc: '/images/badge.png' },
    { id: 3, title: 'Custom Meal Plan', points: 1000, imgSrc: '/images/meal-plan.png' },
    { id: 4, title: 'Free Consultation with Nutritionist', points: 1500, imgSrc: '/images/nutritionist.png' },
    { id: 5, title: 'Exclusive Workout Guide', points: 1200, imgSrc: '/images/workout-guide.png' },
    { id: 6, title: 'Personalized Fitness Tracker', points: 2000, imgSrc: '/images/fitness-tracker.png' },
    { id: 7, title: 'Healthy Snacks Box', points: 700, imgSrc: '/images/snacks-box.png' },
    { id: 8, title: '3-Month Gym Membership', points: 2500, imgSrc: '/images/gym-membership.png' },
    { id: 9, title: 'Stress Relief Kit', points: 600, imgSrc: '/images/stress-relief.png' },
    { id: 10, title: 'Convert to Donation', points: 100, imgSrc: '/images/donation.png' },
  ];

  const handleClaim = (rewardTitle) => {
    alert(`You have claimed: ${rewardTitle}!`);
  };

  return (
    <main className="rewards-page">
      <div className="rewards-container">
        <h2>Rewards</h2>
        <p>Track your progress and claim rewards! Here's what you can redeem:</p>
        <div className="rewards-grid">
          {rewardsData.map((reward) => (
            <div className="reward-card" key={reward.id}>
              {/* Set alt for accessibility but ensure no title appears */}
              <img src={reward.imgSrc} alt={`${reward.title}`} className="reward-img" />
              <h3>{reward.title}</h3>
              <p>{reward.points} Points</p>
              <button onClick={() => handleClaim(reward.title)} className="claim-btn">
                Claim
              </button>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
};

export default Rewards;
