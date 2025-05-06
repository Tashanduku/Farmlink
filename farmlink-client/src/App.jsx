// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './redux/store';

import Layout from './components/common/Layout';
import Welcome from './pages/Welcome';
import Login from './pages/Login';
import SignUp from './pages/Signup';
import Home from './pages/Home';
import BlogDetail from './pages/BlogDetail';
import CreateBlog from './pages/CreateBlog';
import ExpertList from './components/experts/ExpertList';
import CommunityList from './components/communities/CommunityList';
import Profile from './pages/Profile';
import BlogList from './components/blogs/BlogList';

function App() {
  return (
    <Provider store={store}>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            {/* Public routes (now inside Layout) */}
            <Route index element={<Welcome />} />
            <Route path="login" element={<Login />} />
            <Route path="signup" element={<SignUp />} />

            {/* Main app routes */}
            <Route path="home" element={<Home />} />
            <Route path="blogs" element={<BlogList />} />
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




