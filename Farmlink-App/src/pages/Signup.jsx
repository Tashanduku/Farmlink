import React, { useState } from 'react';

const SignUp = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = e => {
    e.preventDefault();
    // handle signup API call here
    console.log("Sign up:", formData);
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md mt-10">
      <h2 className="text-2xl font-semibold mb-4 text-center text-green-700">Create Your Account</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="username"
          onChange={handleChange}
          value={formData.username}
          placeholder="Username"
          className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-green-400"
        />
        <input
          name="email"
          onChange={handleChange}
          value={formData.email}
          type="email"
          placeholder="Email"
          className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-green-400"
        />
        <input
          name="password"
          onChange={handleChange}
          value={formData.password}
          type="password"
          placeholder="Password"
          className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-green-400"
        />
        <button
          type="submit"
          className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700 transition"
        >
          Sign Up
        </button>
      </form>
    </div>
  );
};

export default SignUp;
