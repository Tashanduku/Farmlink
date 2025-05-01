import React from 'react';
import { Link } from 'react-router-dom';

const Welcome = () => {
  return (
    <main className="min-h-screen bg-green-50 flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold mb-6 text-center text-green-800">Welcome to the Farmlink App</h1>
      <p className="text-gray-600 text-center mb-8 max-w-md">
        Centralizing knowledge, community, and expert guidance to support sustainable agriculture.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-sm">
        <Link
          to="/signup"
          className="bg-green-600 text-white py-2 px-4 rounded text-center hover:bg-green-700 shadow-md hover:shadow-lg"
        >
          Sign Up
        </Link>
        <Link
          to="/login"
          className="bg-white border border-green-600 text-green-600 py-2 px-4 rounded text-center hover:bg-green-100 shadow-md hover:shadow-lg"
        >
          Login
        </Link>
        <Link
          to="/blogs"
          className="bg-green-500 text-white py-2 px-4 rounded text-center hover:bg-green-600 shadow-md hover:shadow-lg"
        >
          Blogs
        </Link>
        <Link
          to="/experts"
          className="bg-green-500 text-white py-2 px-4 rounded text-center hover:bg-green-600 shadow-md hover:shadow-lg"
        >
          Experts
        </Link>
        <Link
          to="/communities"
          className="bg-green-500 text-white py-2 px-4 rounded text-center hover:bg-green-600 shadow-md hover:shadow-lg"
        >
          Communities
        </Link>
        <Link
          to="/profile"
          className="bg-white border border-green-500 text-green-700 py-2 px-4 rounded text-center hover:bg-green-100 shadow-md hover:shadow-lg"
        >
          Profile
        </Link>
      </div>
    </main>
  );
};

export default Welcome;
