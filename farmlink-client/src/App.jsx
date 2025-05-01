// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './redux/store';
import Layout from './components/common/Layout';
import Home from './pages/Home';
import BlogDetail from './pages/BlogDetail';
import CreateBlog from './pages/CreateBlog';

function App() {
  return (
    <Provider store={store}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/blogs" element={<Home />} />
            <Route path="/blogs/create" element={<CreateBlog />} />
            <Route path="/blogs/:id" element={<BlogDetail />} />
            <Route path="/community" element={<Home />} />
            <Route path="/experts" element={<Home />} />
            <Route path="/profile" element={<Home />} />
          </Routes>
        </Layout>
      </Router>
    </Provider>
  );
}

export default App;