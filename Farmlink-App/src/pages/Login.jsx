import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: '', password: '' });

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = e => {
    e.preventDefault();
    // replace with real login logic
    console.log("Login:", formData);
    navigate('/profile');
  };

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-semibold mb-4">Login</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input name="username" value={formData.username} onChange={handleChange} placeholder="Username" className="w-full border p-2 rounded" />
        <input name="password" type="password" value={formData.password} onChange={handleChange} placeholder="Password" className="w-full border p-2 rounded" />
        <button type="submit" className="w-full bg-green-600 text-white p-2 rounded">Login</button>
      </form>
    </div>
  );
};

export default Login;
