import React from 'react';
import { useNavigate } from 'react-router-dom';
import FollowButton from '../common/FollowButton';

const CommunityCard = ({ community, loggedInUserId }) => {
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate(`/communities/${community.id}`);
  };

  const handleFollowAndMessage = async (e) => {
    e.stopPropagation(); // prevent card navigation

    try {
      // Follow the community (you could move this logic into FollowButton if preferred)
      await fetch('/api/follow', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          followerId: loggedInUserId,
          communityId: community.id,
        }),
      });

      // Send message or notification to admin
      await fetch('/api/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          senderId: loggedInUserId,
          recipientId: community.admin_id,
          content: `User ${loggedInUserId} just followed your community "${community.name}".`,
        }),
      });

  
    } catch (error) {
      console.error('Error following or sending message:', error);
    }
  };

  return (
    <div
      className="flex items-center p-4 bg-white rounded-lg shadow-sm mb-4 cursor-pointer hover:shadow-md transition-shadow duration-300"
      onClick={handleNavigate}
    >
      <div className="flex basis-3/4">
        <div className="h-12 w-12 rounded-full overflow-hidden mr-4">
          <img
            src={community.image}
            alt={community.name}
            className="h-full w-full object-cover"
          />
        </div>
        <div>
          <h3 className="font-semibold text-gray-800 uppercase">{community.name}</h3>
          <p className="text-xs text-gray-600">WELCOME TO THE COMMUNITY</p>
        </div>
      </div>

      <div className="basis-1/4" onClick={handleFollowAndMessage}>
        <FollowButton currentUserId={loggedInUserId} recipientId={community.admin_id} />
      </div>
    </div>
  );
};

export default CommunityCard;
