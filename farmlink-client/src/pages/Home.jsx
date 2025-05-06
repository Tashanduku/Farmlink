// src/pages/Home.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  // Simulated user data & content (replace with real data in the future)
  const userName = 'Jane Farmer';
  const communities = ['Organic Growers', 'Sustainable Farming', 'AgriTech Innovators'];
  const recentPosts = [
    { id: 1, title: '5 Tips for Better Crop Yields', author: 'Dr. Green' },
    { id: 2, title: 'How to Start Organic Farming', author: 'Farmer Lee' },
    { id: 3, title: 'Pest Control Without Chemicals', author: 'EcoAgri' },
  ];
  const expertRecommendations = [
    'Check soil moisture levels this week.',
    'Join the upcoming webinar on AgriTech.',
    'Review your farm’s financial report.',
  ];

  return (
    <div className="home-container">
      <section className="welcome-section">
        <h2>Welcome back, {userName}! 👋</h2>
        <p>Here’s what’s happening on Farmlink today:</p>
      </section>

      <section className="communities-section">
        <h3>Your Communities</h3>
        <ul>
          {communities.map((community, index) => (
            <li key={index}>{community}</li>
          ))}
        </ul>
        <Link to="/communities" className="btn view-more-btn">View All Communities</Link>
      </section>

      <section className="blog-section">
        <h3>Recent Blog Posts</h3>
        {recentPosts.map(post => (
          <div key={post.id} className="blog-post">
            <h4>{post.title}</h4>
            <p>by {post.author}</p>
            <Link to={`/blogs/${post.id}`} className="read-more-link">Read More</Link>
          </div>
        ))}
        <Link to="/blogs" className="btn view-more-btn">View All Blogs</Link>
      </section>

      <section className="recommendations-section">
        <h3>Expert Recommendations</h3>
        <ul>
          {expertRecommendations.map((rec, index) => (
            <li key={index}>{rec}</li>
          ))}
        </ul>
        <Link to="/experts" className="btn view-more-btn">Ask an Expert</Link>
      </section>
    </div>
  );
};

export default Home;
