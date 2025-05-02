import React from 'react';
import { Link } from 'react-router-dom';
import './Welcome.css'; // ✅ Import the CSS

const Welcome = () => {
  return (
    <div className="welcome-container">
      <h1>Welcome to the Farmlink App</h1>
      <p>
        Centralizing knowledge, community, and expert guidance to support sustainable agriculture.
      </p>

      <div className="welcome-buttons">
        <Link to="/signup" className="welcome-button green">Sign Up</Link>
        <Link to="/login" className="welcome-button white">Login</Link>
        <Link to="/blogs" className="welcome-button green">Blogs</Link>
        <Link to="/experts" className="welcome-button green">Experts</Link>
        <Link to="/communities" className="welcome-button green">Communities</Link>
        <Link to="/profile" className="welcome-button white">Profile</Link>
      </div>
    </div>
  );
};

export default Welcome;
