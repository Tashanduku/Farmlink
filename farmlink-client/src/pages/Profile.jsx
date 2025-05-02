import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Profile.css';

const Profile = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: 'jane_farmer',
    email: 'jane@example.com',
    phone: '+1234567890',
    bio: 'Organic farming enthusiast.',
    profilePic: null,
  });

  const [previewPic, setPreviewPic] = useState(null);

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleImageChange = e => {
    const file = e.target.files[0];
    if (file) {
      setFormData({ ...formData, profilePic: file });
      setPreviewPic(URL.createObjectURL(file));
    }
  };

  const handleSave = e => {
    e.preventDefault();
    console.log('Profile saved:', formData);
    alert('Profile updated successfully!');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  // Simulate recent activity
  const recentActivity = [
    'Commented on "Best Crops for 2025"',
    'Liked "Organic Fertilizer Tips"',
    'Joined Community: Sustainable Farmers',
  ];

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h2>Profile</h2>
        <img
          src={previewPic || 'https://via.placeholder.com/120'}
          alt="Profile"
          className="profile-pic"
        />
        <input type="file" accept="image/*" onChange={handleImageChange} />
      </div>
      <form onSubmit={handleSave}>
        <div className="profile-field">
          <label>Username</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
          />
        </div>
        <div className="profile-field">
          <label>Bio (About)</label>
          <textarea
            name="bio"
            rows="3"
            value={formData.bio}
            onChange={handleChange}
          />
        </div>

        <div className="section">
          <h3>Recent Activity</h3>
          {recentActivity.map((item, index) => (
            <div key={index} className="activity-item">
              {item}
            </div>
          ))}
        </div>

        <div className="section">
          <h3>Socials</h3>
          <div className="profile-field">
            <label>Phone Number</label>
            <input
              type="text"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
            />
          </div>
          <div className="profile-field">
            <label>Email Address</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="button-group">
          <button type="submit" className="button save-button">
            Save Changes
          </button>
          <button type="button" className="button logout-button" onClick={handleLogout}>
            Log Out
          </button>
        </div>
      </form>
    </div>
  );
};

export default Profile;

