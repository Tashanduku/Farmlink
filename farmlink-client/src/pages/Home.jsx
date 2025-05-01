// src/pages/Home.jsx
import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { fetchBlogs } from '../redux/slices/blogSlice';
import BlogList from '../components/blogs/BlogList';
import CommunityList from '../components/communities/CommunityList';
import ExpertList from '../components/experts/ExpertList';

const Home = () => {
  const dispatch = useDispatch();
  const { blogs, status, error } = useSelector((state) => state.blogs);

  useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchBlogs());
    }
  }, [status, dispatch]);

  if (status === 'loading') {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500"></div>
      </div>
    );
  }

  if (status === 'failed') {
    return (
      <div className="flex justify-center items-center h-64">
        <p className="text-red-500">Error: {error}</p>
      </div>
    );
  }

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Blog Section - Takes 2/3 of screen on desktop */}
        <div className="md:col-span-2">
          
          <BlogList />
        </div>
        
        {/* Right Column - Takes 1/3 of screen on desktop */}
        <div className="space-y-8">
          <CommunityList />
          <ExpertList />
        </div>
      </div>
    </>
  );
};

export default Home;