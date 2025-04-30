import React from 'react';
import { Link } from 'react-router-dom';

const Welcome = () => {
  return (
    <div className="min-h-screen bg-green-50 flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold mb-4 text-center">Welcome to the Farmlink App</h1>
      <p className="text-gray-600 text-center mb-6 max-w-md">
        Centralizing knowledge, community, and expert guidance to support sustainable agriculture.
      </p>

      <div className="grid grid-cols-2 gap-4 w-full max-w-sm">
        <Link to="/signup" className="bg-green-600 text-white py-2 px-4 rounded text-center hover:bg-green-700">Sign Up</Link>
        <Link to="/login" className="bg-white border border-green-600 text-green-600 py-2 px-4 rounded text-center hover:bg-green-100">Login</Link>
        <Link to="/blogs" className="bg-green-500 text-white py-2 px-4 rounded text-center hover:bg-green-600">Blogs</Link>
        <Link to="/experts" className="bg-green-500 text-white py-2 px-4 rounded text-center hover:bg-green-600">Experts</Link>
        <Link to="/communities" className="bg-green-500 text-white py-2 px-4 rounded text-center hover:bg-green-600">Communities</Link>
        <Link to="/profile" className="bg-white border border-green-500 text-green-700 py-2 px-4 rounded text-center hover:bg-green-100">Profile</Link>
      </div>
    </div>
  );
};

export default Welcome;
