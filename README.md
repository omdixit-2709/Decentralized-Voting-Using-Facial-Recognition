# Blockchain-Based Voting System with Facial Recognition

## Overview
This project implements a secure and transparent voting system using blockchain and AI-driven facial recognition. It leverages blockchain technology (Ethereum) for storing votes and facial recognition for authenticating voters in a real-time environment. The system ensures that only legitimate voters are authenticated and their votes are securely cast, providing a tamper-proof voting experience.

## Features
- **Face Authentication**: Uses face recognition to authenticate voters, ensuring only authorized users can cast their votes.
- **Blockchain Voting**: Integrates Ethereum smart contracts to securely record votes, ensuring transparency and preventing fraud.
- **Secure Backend**: Built with Flask to handle face recognition and blockchain interactions.
- **Frontend Interface**: Developed using ReactJS to provide a seamless user experience for voters to authenticate and vote.
- **Privacy**: Transactions are signed and executed securely using Web3 and Ethereum’s decentralized network.
- **Real-time Voting**: The system allows users to cast votes in real-time through a secure and private interface.

## Technologies
- **Backend**: Python, Flask
- **Frontend**: ReactJS
- **Blockchain**: Ethereum, Web3
- **Face Recognition**: face_recognition, OpenCV
- **Smart Contracts**: Solidity
- **Libraries**: axios, Web3.js

## Setup Instructions

### Prerequisites
- Python 3.x
- Node.js and npm
- Ethereum client (e.g., Ganache or Infura for remote node)
- Web3.py for Python
- Web3.js for React

### Backend Setup (Flask & Facial Recognition)
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/blockchain-voting-facial-recognition.git
   cd blockchain-voting-facial-recognition


How It Works
Voter Authentication
Voters upload an image of their face, which is processed using the face_recognition library to compare it with pre-registered faces stored in the voter_data/ folder.
If a match is found, the voter is authenticated, and they are allowed to proceed with casting their vote.
Casting Votes on Blockchain
Once authenticated, the voter selects their desired candidate.
The vote is recorded on the Ethereum blockchain by interacting with a deployed smart contract using Web3.
Each vote is associated with a transaction hash to provide proof of the vote.

Smart Contract

Here’s a simple example of a Solidity smart contract for voting:

pragma solidity ^0.8.0;

contract Voting {
    mapping(address => bool) public hasVoted;
    mapping(uint => uint) public votesReceived;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function vote(uint candidateId) public {
        require(!hasVoted[msg.sender], "You have already voted.");
        votesReceived[candidateId] += 1;
        hasVoted[msg.sender] = true;
    }

    function totalVotesFor(uint candidateId) public view returns (uint) {
        return votesReceived[candidateId];
    }
}
Contributions
Feel free to fork the repository, submit issues, or open pull requests. Contributions are welcome!
