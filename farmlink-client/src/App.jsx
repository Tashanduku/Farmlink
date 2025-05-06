import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './redux/store';
import { AuthProvider } from './contexts/AuthContext';

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
import BlogList from './components/blogs/BlogList';  // Updated to import BlogList

// Private route component
const PrivateRoute = ({ element }) => {
  const isAuthenticated = localStorage.getItem('token') !== null;
  return isAuthenticated ? element : <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Provider store={store}>
          <Routes>
            <Route path="/" element={<Layout />}>
              {/* Public routes */}
              <Route index element={<Welcome />} />
              <Route path="login" element={<Login />} />
              <Route path="signup" element={<SignUp />} />

              {/* Protected routes */}
              <Route path="home" element={<PrivateRoute element={<Home />} />} />
              <Route path="blogs" element={<PrivateRoute element={<BlogList />} />} /> {/* Updated this route */}
              <Route path="blogs/create" element={<PrivateRoute element={<CreateBlog />} />} />
              <Route path="blogs/:id" element={<BlogDetail />} />
              <Route path="communities" element={<PrivateRoute element={<CommunityList />} />} />
              <Route path="experts" element={<ExpertList />} />
              <Route path="profile" element={<PrivateRoute element={<Profile />} />} />
            </Route>
          </Routes>
        </Provider>
      </Router>
    </AuthProvider>
  );
}

export default App;
