import React from 'react';

const Profile = () => {
  const user = {
    username: "jane_farmer",
    email: "jane@example.com",
    bio: "Organic farming enthusiast."
  };

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Profile</h2>
      <p><strong>Username:</strong> {user.username}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Bio:</strong> {user.bio}</p>
    </div>
  );
};

export default Profile;

