import React, { useState, useEffect } from 'react';
import CommunityCard from './CommunityCard';
import communitiesData from '../../data/communities.json';

const CommunityList = () => {
  const [communities, setCommunities] = useState([]);

  useEffect(() => {
    // In a real app, this would be an API call
    setCommunities(communitiesData.communities);
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">COMMUNITIES</h1>
      <div className="grid grid-cols-1 gap-4">
        {communities.map(community => (
          <CommunityCard key={community.id} community={community} />
        ))}
      </div>
    </div>
  );
};

export default CommunityList;