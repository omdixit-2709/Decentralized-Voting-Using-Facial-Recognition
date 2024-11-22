import React, { useState } from 'react';
import axios from 'axios';

const VotingInterface = () => {
  const [candidate, setCandidate] = useState('');
  const [voteStatus, setVoteStatus] = useState('');

  const handleVote = async () => {
    const voterAddress = 'USER_VOTER_ADDRESS';  // This should come from the authentication process

    try {
      const response = await axios.post('http://localhost:5000/cast_vote', {
        voter_address: voterAddress,
        candidate_id: candidate
      });

      if (response.data.status === 'success') {
        setVoteStatus('Vote successfully cast!');
      } else {
        setVoteStatus('Error casting vote');
      }
    } catch (error) {
      setVoteStatus('Error during voting');
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Vote for your Candidate</h2>
      <input 
        type="text" 
        value={candidate} 
        onChange={e => setCandidate(e.target.value)} 
        placeholder="Enter Candidate ID" 
      />
      <button onClick={handleVote}>Cast Vote</button>
      <p>{voteStatus}</p>
    </div>
  );
};

export default VotingInterface;
