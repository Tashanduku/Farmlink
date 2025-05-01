// src/components/common/Layout.jsx
import React from 'react';
import NavBar from './NavBar';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <NavBar />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  );
};

export default Layout;