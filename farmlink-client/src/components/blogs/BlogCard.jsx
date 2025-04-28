import React from 'react';
import { useNavigate } from 'react-router-dom';

const BlogCard = ({ blog }) => {
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate(`/blogs/${blog.id}`);
  };

  return (
    <div 
      className="bg-white mb-8 pb-6 border-b border-gray-100 cursor-pointer hover:shadow-sm transition-shadow duration-300" 
      onClick={handleNavigate}
    >
      <div className="flex flex-col md:flex-row">
        <div className="md:w-3/4 pr-6">
          <h2 className="text-2xl font-extrabold uppercase mb-3 tracking-wide">{blog.title}</h2>
          <p className="text-sm text-gray-700 mb-4 leading-relaxed">
            {blog.summary || blog.content.substring(0, 150) + '...'}
          </p>
          <div className="flex items-center text-xs text-gray-600 mb-4">
            <span className="mr-4">By {blog.author}</span>
            <span>{new Date(blog.date).toLocaleDateString()}</span>
          </div>
          <div className="flex justify-between items-center mt-4">
            <div className="flex space-x-4">
              <button 
                className="flex items-center text-gray-600 hover:text-green-500"
                onClick={(e) => {
                  e.stopPropagation();
                  // Like functionality
                }}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
                <span>{blog.likes}</span>
              </button>
              <button 
                className="flex items-center text-gray-600 hover:text-green-500"
                onClick={(e) => {
                  e.stopPropagation();
                  // Comment functionality
                }}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                <span>{blog.comments}</span>
              </button>
            </div>
            <button 
              className="text-green-600 hover:text-green-800 font-medium"
              onClick={(e) => {
                e.stopPropagation();
                handleNavigate();
              }}
            >
              Read More
            </button>
          </div>
        </div>
        <div className="md:w-1/4 mt-4 md:mt-0">
          <img 
            src={blog.image} 
            alt={blog.title} 
            className="w-full h-40 object-cover rounded-md"
          />
        </div>
      </div>
    </div>
  );
};

export default BlogCard;