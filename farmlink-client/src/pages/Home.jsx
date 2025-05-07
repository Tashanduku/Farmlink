import React from 'react';
import NavBar from '../components/common/NavBar';
import BlogList from '../components/blogs/BlogList';
import CommunityList from '../components/communities/CommunityList';
import ExpertList from '../components/experts/ExpertList';

const Home = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <NavBar />
      
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-2">
            <BlogList />
          </div>
          
          <div className="space-y-8">
            <CommunityList />
            <ExpertList />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;