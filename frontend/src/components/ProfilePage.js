import React, { useState } from 'react';
import '../styles/ProfilePage.css'; // Add this file for custom styles if needed

const Profile = () => {
  const [editMode, setEditMode] = useState(false);

  const handleEditClick = () => {
    setEditMode(!editMode);
  };

  return (
    <main className="profile-page">
      <div className="profile-container">
        {/* Profile Header Section */}
        <div className="profile-header">
          <div className="profile-picture">
            <img 
              src="/default-profile-picture.png" 
              alt="Profile" 
              className="profile-img" 
            />
          </div>
          <div className="profile-info">
            <h2>John Doe</h2>
            <p>Email: johndoe@example.com</p>
            <p>Member since: January 2022</p>
            <button className="edit-btn" onClick={handleEditClick}>
              {editMode ? 'Save' : 'Edit Profile'}
            </button>
          </div>
        </div>

        {/* Profile Tabs */}
        <div className="profile-tabs">
          <button className="tab-btn active">Personal Info</button>
          <button className="tab-btn">Settings</button>
          <button className="tab-btn">Activity</button>
        </div>

        {/* Profile Content Section */}
        <div className="profile-content">
          {editMode ? (
            <div className="edit-section">
              <h3>Edit Your Information</h3>
              <label>
                Name:
                <input type="text" value="John Doe" />
              </label>
              <label>
                Email:
                <input type="email" value="johndoe@example.com" />
              </label>
              <label>
                Member Since:
                <input type="text" value="January 2022" disabled />
              </label>
            </div>
          ) : (
            <div className="info-section">
              <h3>Personal Information</h3>
              <p><span>Name:</span> John Doe</p>
              <p><span>Email:</span> johndoe@example.com</p>
              <p><span>Member since:</span> January 2022</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
};

export default Profile;
