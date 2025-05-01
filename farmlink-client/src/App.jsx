import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import BlogDetail from './pages/BlogDetail';
import ExpertList from './components/experts/ExpertList';
import CommunityList from './components/communities/CommunityList'; // ✅ Add this import

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/blogs" element={<BlogDetail />} />
        <Route path="/communities" element={<CommunityList />} />
        <Route path='/experts' element={<ExpertList/>} />
      </Routes>
    </Router>
  );
}

export default App;
