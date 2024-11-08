import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import Loader from '../Loader/Loader';

export default function Analysis({ onFileAnalyzed }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [confidence, setConfidence] = useState('');
  const [emotionResult, setEmotionResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles, rejectedFiles) => {
      if (rejectedFiles.length > 0) {
        rejectedFiles.forEach((file) => {
          console.warn(`Rejected: ${file.name} with extension ${file.name.split('.').pop()}`);
        });
      }

      if (acceptedFiles.length > 0) {
        const fileData = acceptedFiles[0];
        setSelectedFile(fileData);
      }
    },
    accept: 'video/*,image/*',
    maxFiles: 1,
  });

  const handleSubmit = async () => {
    if (!selectedFile) {
      alert('Please upload a video or image file');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/Detect', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      console.log("Response from backend:", response.data);
      setResult(response.data.deepfake_result.result);
      setConfidence(response.data.deepfake_result.confidence);
      setEmotionResult(response.data.emotion_result);
      console.log('Emotion Result:', response.data.emotion_result);

      // Pass the analyzed file data to the parent component
      onFileAnalyzed({
        file: selectedFile,
        name: selectedFile.name,
        type: selectedFile.type,
        result: response.data.deepfake_result.result,
        confidence: response.data.deepfake_result.confidence,
        emotion_result: response.data.emotion_result,
      });
    } catch (error) {
      console.error('Error during detection:', error);
      setResult('Error during detection');
      setConfidence('N/A');
      setEmotionResult('Audio unavailable');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setResult(null);
    setConfidence('');
    setEmotionResult(null);
  };

  return (
    <div className="flex justify-center mt-8">
      <div className="max-w-md w-full bg-base-200 shadow-lg rounded-lg overflow-hidden">
        <div className="px-6 py-6">
          <h1 className="text-2xl font-bold text-base-content">DeepFake Detector</h1>
          <p className="text-base-content mt-2">
            Upload a video or image to check if it's fake using our AI detection system.
          </p>

          {/* Drag-and-Drop Area */}
          {!selectedFile && (
            <div
              {...getRootProps()}
              className={`mt-4 flex flex-col items-center justify-center p-6 border-2 border-dashed rounded cursor-pointer ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-100'}`}
            >
              <input {...getInputProps()} />
              {isDragActive ? (
                <p className="text-blue-500">Drop the file here...</p>
              ) : (
                <p className="text-gray-600">Drag & drop a file here, or click to select a file</p>
              )}
            </div>
          )}

          {/* Preview Section */}
          {selectedFile && (
            <div className="mt-4">
              <p className="text-base-content mb-2">Preview:</p>
              {selectedFile.type.startsWith('image') ? (
                <img
                  src={URL.createObjectURL(selectedFile)}
                  alt="Preview"
                  className="w-full h-64 object-cover rounded"
                />
              ) : (
                <video
                  src={URL.createObjectURL(selectedFile)}
                  controls
                  className="w-full h-64 rounded"
                />
              )}
              {/* Toggle Button */}
              <button
                onClick={result === null ? handleSubmit : handleReset}
                className={`mt-4 w-full py-2 px-4 ${result === null ? 'bg-green-500 hover:bg-green-600' : 'bg-blue-500 hover:bg-blue-600'} text-white font-semibold rounded ${loading ? 'cursor-not-allowed' : ''}`}
                disabled={loading}
              >
                {loading ? 'Detecting...' : result === null ? 'Analyze Media' : 'Upload Another File'}
              </button>
            </div>
          )}

          {/* Loader */}
          {loading && (
            <div className="mt-4">
              <Loader filename={selectedFile.name} isComplete={result !== null} />
            </div>
          )}

          {/* Results Section */}
          {result !== null && (
            <div className="mt-6">
              <h3 className="text-xl font-semibold text-base-content">Detection Result</h3>
              <p className="text-base-content mt-2">
                Result: <strong>{result}</strong>
              </p>
              <p className="text-base-content mt-1">
                Confidence: <strong>{confidence}%</strong>
              </p>
              {emotionResult && (
                <div className="mt-4">
                  <p>
                    Emotion: <strong>{emotionResult.emotion}</strong><br />
                    Score: <strong>{emotionResult.score}</strong><br />
                    Transcribed Text: <strong>{emotionResult.transcribed_text}</strong>
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
