import React, { useState } from 'react';
import axios from 'axios';
import './analysis.css'; // Assuming you have the necessary styles
import Loader from '../Loader/Loader'; // Import your loader

export default function Analysis() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState('');
  const [confidence, setConfidence] = useState('');
  const [emotions, setEmotions] = useState([]); // State for emotions array
  const [loading, setLoading] = useState(false); // State to track loading status
  const videoFilename = "your_video_file.mp4"; 

  const emojiMap = {
    0: "😊",  // Happy
    1: "😢",  // Sad
    2: "😡",  // Angry
    3: "😐",  // Neutral
    4: "😲"   // Surprised
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      alert("Please upload a video file");
      return;
    }

    setLoading(true); // Start showing loader
    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      // Make sure the request goes to the Flask server
      const response = await axios.post('http://localhost:5000/Detect', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Handle the response: Accessing 'result', 'confidence', and 'emotions'
      console.log('Success:', response.data);
      setResult(response.data.result); 
      setConfidence(response.data.confidence); 
      setEmotions(response.data.emotions); 

    } catch (error) {
      console.error("Error while uploading file:", error);
      setResult("Error during detection");
      setConfidence("N/A");
      setEmotions([]); 
    } finally {
      setLoading(false); // Stop showing loader
    }
  };

  return (
    <div className="app-container">
      <div className="content">
        <h1 className="app-title">DeepFake Detector</h1>
        <p className="app-description">Upload a video and check if it is fake using our advanced AI detection system.</p>
        
        <input 
          type="file" 
          accept="video/*" 
          id="videoUpload" 
          onChange={handleFileChange}
          style={{ display: 'none' }} 
        />
        <label htmlFor="videoUpload" className="upload-btn">
          + Add Video
        </label>

        {selectedFile && <p className="file-name">File: {selectedFile.name}</p>}

        <button onClick={handleSubmit} className="detect-btn" disabled={loading}>
          {loading ? "Detecting..." : "Detect"}
        </button>

        {/* Show loader while the request is being processed */}
        {loading && (
          <div className="loader-container">
             <Loader filename={videoFilename} />
          </div>
        )}

        {/* Show the result when detection is complete */}
        <div className="result-area">
          <h3 className="result-title">Detection Result</h3>
          {result ? (
            <>
              <p className="result-text">Result: <strong>{result}</strong></p>
              <p className="confidence-text">Confidence: <strong>{confidence}%</strong></p>
              
              {/* Display the emotions as emojis */}
              <div className="emotion-display">
                <h3>Detected Emotions:</h3>
                {emotions.length > 0 ? (
                  emotions.map((emotion, index) => (
                    <span key={index} className="emotion-emoji">
                      {emojiMap[emotion.emotion]} ({emotion.confidence.toFixed(2)}%)
                    </span>
                  ))
                ) : (
                  <p>No emotions detected.</p>
                )}
              </div>
            </>
          ) : (
            <p className="no-result">Upload a video to see the result.</p>
          )}
        </div>
      </div>
    </div>
  );
}
