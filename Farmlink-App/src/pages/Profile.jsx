import React from 'react';
import { useNavigate } from 'react-router-dom';

const Profile = () => {
  const navigate = useNavigate();

  const user = {
    username: 'jane_farmer',
    email: 'jane@example.com',
    bio: 'Organic farming enthusiast.',
  };

  const handleLogout = () => {
    // Example: Clear auth data (if you have any in localStorage)
    localStorage.removeItem('token'); // remove token if using token-based auth
    // Navigate to login or welcome page
    navigate('/login');
  };

  return (
    <div className="max-w-md mx-auto p-6 min-h-screen flex flex-col justify-center bg-green-50">
      <h2 className="text-2xl font-bold mb-4 text-center">Profile</h2>
      <div className="bg-white shadow rounded p-4 mb-6">
        <p><strong>Username:</strong> {user.username}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Bio:</strong> {user.bio}</p>
      </div>
      <button
        onClick={handleLogout}
        className="bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700 mx-auto"
      >
        Log Out
      </button>
    </div>
  );
};

export default Profile;

