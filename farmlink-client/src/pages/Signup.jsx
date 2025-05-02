import React, { useState } from 'react';
import './Signup.css'; // Import your CSS file ✅

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
    console.log("Sign up:", formData);
  };

  return (
    <div className="signup-container">
      <h2>Create Your Account</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="username"
          onChange={handleChange}
          value={formData.username}
          placeholder="Username"
        />
        <input
          name="email"
          onChange={handleChange}
          value={formData.email}
          type="email"
          placeholder="Email"
        />
        <input
          name="password"
          onChange={handleChange}
          value={formData.password}
          type="password"
          placeholder="Password"
        />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
};

export default SignUp;
