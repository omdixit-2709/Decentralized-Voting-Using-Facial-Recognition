import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FacialRecognition = () => {
  const [status, setStatus] = useState('');
  const [userName, setUserName] = useState('');
  const [videoStream, setVideoStream] = useState(null);

  useEffect(() => {
    const startVideo = async () => {
      const video = document.getElementById('video');
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      video.srcObject = stream;
      setVideoStream(stream);
    };
    startVideo();
    return () => {
      if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop()); // Stop video stream on component unmount
      }
    };
  }, [videoStream]);

  const handleCapture = async () => {
    const video = document.getElementById('video');
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, 640, 480);
    const imageData = canvas.toDataURL('image/jpeg');

    try {
      const response = await axios.post('http://localhost:5000/authenticate', {
        image: imageData
      });

      if (response.data.status === 'success') {
        setUserName(response.data.name);
        setStatus('Authenticated');
      } else {
        setStatus('Authentication Failed');
      }
    } catch (error) {
      setStatus('Error during authentication');
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Facial Recognition Login</h2>
      <video id="video" width="640" height="480" autoPlay></video>
      <button onClick={handleCapture}>Capture and Authenticate</button>
      <p>Status: {status}</p>
      {userName && <p>Welcome {userName}</p>}
    </div>
  );
};

export default FacialRecognition;
