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
    localStorage.removeItem('token'); // remove token if using token-based auth
    alert('You have been logged out.');
    navigate('/login');
  };

  return (
    <div className="max-w-md mx-auto p-6 min-h-screen flex flex-col justify-center items-center bg-green-50">
      <h2 className="text-2xl font-bold mb-4 text-center text-green-700">Profile</h2>
      <div className="bg-white shadow rounded p-4 mb-6 w-full">
        <p className="mb-2"><strong>Username:</strong> {user.username}</p>
        <p className="mb-2"><strong>Email:</strong> {user.email}</p>
        <p><strong>Bio:</strong> {user.bio}</p>
      </div>
      <button
        onClick={handleLogout}
        className="bg-red-600 text-white py-2 px-6 rounded hover:bg-red-700 transition"
      >
        Log Out
      </button>
    </div>
  );
};

export default Profile;
