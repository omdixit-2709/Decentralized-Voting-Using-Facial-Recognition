// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    mapping(address => bool) public voters;
    mapping(address => uint) public votes;
    uint public totalVotes;

    // Register voter address
    function registerVoter() public {
        require(!voters[msg.sender], "Voter already registered");
        voters[msg.sender] = true;
    }

    // Cast a vote
    function castVote(uint candidateId) public {
        require(voters[msg.sender], "Not registered to vote");
        require(votes[msg.sender] == 0, "You have already voted");
        votes[msg.sender] = candidateId;
        totalVotes++;
    }

    // Get the total votes for a candidate
    function getVotes(uint candidateId) public view returns (uint) {
        uint voteCount = 0;
        for (uint i = 0; i < totalVotes; i++) {
            if (votes[msg.sender] == candidateId) {
                voteCount++;
            }
        }
        return voteCount;
    }
}
