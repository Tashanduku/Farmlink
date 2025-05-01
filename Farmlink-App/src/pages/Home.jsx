import React from 'react';
import BlogCard from '../components/BlogCard';

const Home = () => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Latest Agricultural Blogs</h1>
      <BlogCard
        title="Sustainable Farming in 2025"
        author="Prudence Canva"
        likes={34}
        image="https://via.placeholder.com/300x200"
      />
    </div>
  );
};

export default Home;

