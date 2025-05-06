import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './redux/store';
import axios from 'axios';

import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/common/PrivateRoute';
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

// Set default base URL for API requests
axios.defaults.baseURL = 'http://localhost:5000'; // Adjust this to your API URL

function App() {
  return (
    <Provider store={store}>
      <AuthProvider>
        <Router>
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<Layout />}>
              <Route index element={<Welcome />} />
              <Route path="login" element={<Login />} />
              <Route path="signup" element={<SignUp />} />
            </Route>
            
            {/* Protected routes */}
            <Route element={<PrivateRoute />}>
              <Route path="/" element={<Layout />}>
                <Route path="home" element={<Home />} />
                <Route path="blogs" element={<Home />} />
                <Route path="blogs/create" element={<CreateBlog />} />
                <Route path="blogs/:id" element={<BlogDetail />} />
                <Route path="communities" element={<CommunityList />} />
                <Route path="experts" element={<ExpertList />} />
                <Route path="profile" element={<Profile />} />
              </Route>
            </Route>
            
            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </Router>
      </AuthProvider>
    </Provider>
  );
}

export default App;