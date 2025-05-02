// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './redux/store';

import Layout from './components/common/Layout';
import Home from './pages/Home';
import BlogDetail from './pages/BlogDetail';
import CreateBlog from './pages/CreateBlog';
import ExpertList from './components/experts/ExpertList';
import CommunityList from './components/communities/CommunityList';
import Profile from './pages/Profile';
import Welcome from './pages/Welcome';
import Login from './pages/Login';
import Signup from './pages/Signup';

function App() {
  return (
    <Provider store={store}>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Welcome />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          {/* Protected Routes inside Layout */}
          <Route path="/" element={<Layout />}>
            <Route path="home" element={<Home />} />
            <Route path="blogs" element={<Home />} />
            <Route path="blogs/create" element={<CreateBlog />} />
            <Route path="blogs/:id" element={<BlogDetail />} />
            <Route path="communities" element={<CommunityList />} />
            <Route path="experts" element={<ExpertList />} />
            <Route path="profile" element={<Profile />} />
          </Route>
        </Routes>
      </Router>
    </Provider>
  );
}

export default App;

