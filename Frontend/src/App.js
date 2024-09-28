import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Assuming you add the necessary styles
import Loader from './Component/Loader/Loader';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState('');
  const [confidence, setConfidence] = useState('');
  const [loading, setLoading] = useState(false); // State to track loading status

  // Function to handle file input
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Function to submit file to backend
  const handleSubmit = async () => {
    if (!selectedFile) {
      alert("Please upload a video file");
      return;
    }

    setLoading(true); // Show loader when detection starts
    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      // Make sure the request goes to the Flask server at localhost:5000 (or your Flask server's address)
      const response = await axios.post('http://localhost:5000/Detect', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Handle the response: Accessing 'result' and 'confidence'
      console.log('Success:', response.data);
      setResult(response.data.result); // Assuming the backend sends 'result'
      setConfidence(response.data.confidence); // Assuming the backend sends 'confidence'
    } catch (error) {
      console.error("Error while uploading file:", error);
      setResult("Error during detection");
      setConfidence("N/A");
    } finally {
      setLoading(false); // Hide loader when detection completes
    }
  };

  return (
    <div className="app-container">
      <div className="content">
        <h1 className="app-title">Fake Video Detector</h1>
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

        {loading && <Loader />}

        <div className="result-area">
          <h3 className="result-title">Detection Result</h3>
          {result ? (
            <>
              <p className="result-text">Result: <strong>{result}</strong></p>
              <p className="confidence-text">Confidence: <strong>{confidence}%</strong></p>
            </>
          ) : (
            <p className="no-result">Upload a video to see the result.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
