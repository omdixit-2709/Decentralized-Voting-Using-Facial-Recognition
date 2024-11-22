import os
import cv2
import numpy as np
from flask import Flask, request, jsonify
import face_recognition
from web3 import Web3

app = Flask(__name__)

# Path to save voter data (images should be pre-registered in 'voter_data/')
voter_data_path = 'voter_data/'

# Load known faces and names for authentication
known_faces = []
known_names = []

def load_known_faces():
    """Load voter faces and names from the stored images."""
    global known_faces, known_names
    for filename in os.listdir(voter_data_path):
        if filename.endswith(".jpg"):
            name = filename.split('.')[0]  # Use filename (without extension) as voter name
            try:
                image = face_recognition.load_image_file(os.path.join(voter_data_path, filename))
                encoding = face_recognition.face_encodings(image)[0]  # Extract face encoding
                known_faces.append(encoding)
                known_names.append(name)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

# Initialize known faces data
load_known_faces()

@app.route('/authenticate', methods=['POST'])
def authenticate():
    """Authenticate a user's face using facial recognition."""
    try:
        # Receive the image from the request
        data = request.files['image']
        img = cv2.imdecode(np.fromstring(data.read(), np.uint8), cv2.IMREAD_COLOR)
        rgb_img = img[:, :, ::-1]  # Convert from BGR to RGB

        # Detect faces in the uploaded image
        face_locations = face_recognition.face_locations(rgb_img)
        face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

        for encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces, encoding)
            if True in matches:
                name = known_names[matches.index(True)]
                return jsonify({'status': 'success', 'name': name})
        
        return jsonify({'status': 'failure', 'message': 'Face not recognized'})

    except Exception as e:
        return jsonify({'status': 'failure', 'message': str(e)})

# Initialize Web3 connection to Ethereum (for voting)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
contract_address = "YOUR_CONTRACT_ADDRESS"
contract_abi = [{"constant": False, "inputs": [{"name": "_candidateId", "type": "uint256"}], "name": "castVote", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}]

# Load the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    """Cast a vote to a specific candidate on the blockchain."""
    try:
        data = request.json
        voter_address = data['voter_address']
        candidate_id = data['candidate_id']

        # Check if the voter address is valid (example: a simple address length check)
        if len(voter_address) != 42:
            return jsonify({'status': 'failure', 'message': 'Invalid voter address'})

        # Interact with the smart contract to cast a vote
        tx = contract.functions.castVote(candidate_id).buildTransaction({
            'from': voter_address,
            'gas': 2000000,
            'gasPrice': w3.toWei('20', 'gwei'),
            'nonce': w3.eth.getTransactionCount(voter_address),
        })

        # Use private key securely (ensure private key is never hardcoded in production)
        private_key = "YOUR_PRIVATE_KEY"
        signed_tx = w3.eth.account.signTransaction(tx, private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        return jsonify({'status': 'success', 'transaction_hash': tx_hash.hex()})
    
    except Exception as e:
        return jsonify({'status': 'failure', 'message': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
