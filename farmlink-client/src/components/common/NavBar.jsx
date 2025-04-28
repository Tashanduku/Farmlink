import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <nav className="bg-white flex justify-between items-center p-4 border-b">
      <div className="flex items-center">
        <div className="mr-6">
          <img src="/images/logo.svg" alt="Logo" className="h-8" />
        </div>
      </div>
      
      <div className="flex space-x-6 text-lg font-medium">
        <Link to="/" className="hover:text-green-600">CREATE</Link>
        <Link to="/logout" className="hover:text-green-600">LOG OUT</Link>
        <Link to="/blogs" className="hover:text-green-600">BLOGS</Link>
        <Link to="/community" className="hover:text-green-600">COMMUNITY</Link>
        <Link to="/experts" className="hover:text-green-600">EXPERTS</Link>
        <Link to="/profile" className="hover:text-green-600">PROFILE</Link>
      </div>
    </nav>
  );
};

export default NavBar;