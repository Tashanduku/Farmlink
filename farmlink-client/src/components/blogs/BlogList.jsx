import React, { useState, useEffect } from 'react';
import BlogCard from './BlogCard';
import blogsData from '../../data/blogs.json';

const BlogList = () => {
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, this would be an API call
    // Adding a small delay to simulate API fetch
    const loadBlogs = async () => {
      try {
        // Simulating network request
        setTimeout(() => {
          setBlogs(blogsData.blogs);
          setLoading(false);
        }, 500);
      } catch (error) {
        console.log("Error loading blogs:", error);
        setLoading(false);
      }
    };
    
    loadBlogs();
  }, []);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 uppercase text-center md:text-left">Agricultural Blogs</h1>
      <div className="max-w-4xl mx-auto">
        {blogs.length > 0 ? (
          blogs.map(blog => (
            <BlogCard key={blog.id} blog={blog} />
          ))
        ) : (
          <p className="text-center text-gray-500">No blogs found.</p>
        )}
      </div>
    </div>
  );
};

export default BlogList;