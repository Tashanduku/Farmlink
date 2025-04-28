import React, { useState, useEffect } from 'react';
import ExpertCard from './ExpertCard';
import expertsData from '../../data/experts.json';

const ExpertList = () => {
  const [experts, setExperts] = useState([]);

  useEffect(() => {
    // In a real app, this would be an API call
    setExperts(expertsData.experts);
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">EXPERTS</h1>
      <div className="grid grid-cols-1 gap-4">
        {experts.map(expert => (
          <ExpertCard key={expert.id} expert={expert} />
        ))}
      </div>
    </div>
  );
};

export default ExpertList;