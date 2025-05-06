import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Profile.css';

const Profile = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    full_name: '',
    bio: '',
    location: '',
    expertise: '',
    profile_picture: '',
    password: '' // For changing password
  });

  const [previewPic, setPreviewPic] = useState(null);
  
  // Get user ID from localStorage
  const userId = localStorage.getItem('userId');
  const token = localStorage.getItem('token');

  // Fetch user profile data
  useEffect(() => {
    // Check if user is logged in
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchProfile = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/users/${userId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          if (response.status === 401) {
            // Token expired, redirect to login
            localStorage.removeItem('token');
            navigate('/login');
            return;
          }
          throw new Error('Failed to fetch profile');
        }

        const profileData = await response.json();
        
        // Update form data with profile information
        setFormData({
          ...formData,
          username: profileData.username,
          email: profileData.email,
          full_name: profileData.full_name || '',
          bio: profileData.bio || '',
          location: profileData.location || '',
          expertise: profileData.expertise || '',
          profile_picture: profileData.profile_picture || '',
          password: '' // Reset password field
        });

        // Set profile picture preview if available
        if (profileData.profile_picture) {
          setPreviewPic(profileData.profile_picture);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfile();
  }, [userId, token, navigate]);

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleImageChange = e => {
    const file = e.target.files[0];
    if (file) {
      // Create a preview for display
      setPreviewPic(URL.createObjectURL(file));
      
      // Convert to base64 for sending to API
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData({ ...formData, profile_picture: reader.result });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');
    setIsLoading(true);

    try {
      // Create a copy of form data without empty password
      const dataToSend = {...formData};
      if (!dataToSend.password) {
        delete dataToSend.password;
      }

      const response = await fetch(`http://localhost:5000/api/users/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(dataToSend),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to update profile');
      }

      setSuccessMessage('Profile updated successfully!');
      // Reset password field
      setFormData({...formData, password: ''});
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    // Clear all authentication data
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
    navigate('/login');
  };

  if (isLoading && !formData.username) {
    return <div className="loading">Loading profile...</div>;
  }

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

      {error && <div className="error-message">{error}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}

      <form onSubmit={handleSave}>
        <div className="profile-field">
          <label>Username</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            disabled // Username usually can't be changed after registration
          />
        </div>

        <div className="profile-field">
          <label>Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            disabled // Email usually can't be changed easily
          />
        </div>

        <div className="profile-field">
          <label>Full Name</label>
          <input
            type="text"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
          />
        </div>

        <div className="profile-field">
          <label>Bio</label>
          <textarea
            name="bio"
            rows="3"
            value={formData.bio}
            onChange={handleChange}
          />
        </div>

        <div className="profile-field">
          <label>Location</label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
          />
        </div>

        <div className="profile-field">
          <label>Expertise</label>
          <input
            type="text"
            name="expertise"
            value={formData.expertise}
            onChange={handleChange}
          />
        </div>

        <div className="profile-field">
          <label>New Password (leave blank to keep current)</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter new password"
          />
        </div>

        <div className="button-group">
          <button type="submit" className="button save-button" disabled={isLoading}>
            {isLoading ? 'Saving...' : 'Save Changes'}
          </button>
          <button 
            type="button" 
            className="button logout-button" 
            onClick={handleLogout}
          >
            Log Out
          </button>
        </div>
      </form>
    </div>
  );
};

export default Profile;