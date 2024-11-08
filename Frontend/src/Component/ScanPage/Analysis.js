import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import Loader from '../Loader/Loader';

export default function Analysis({ onFileAnalyzed }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [mediaType, setMediaType] = useState(null);
  const [result, setResult] = useState(null);
  const [confidence, setConfidence] = useState('');
  const [emotionResult, setEmotionResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles) => {
      const fileData = acceptedFiles[0];
      setSelectedFile(fileData);
      setMediaType(fileData.type.startsWith('image') ? 'image' : 'video');
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
    formData.append('media', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/Detect', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      console.log("Response from backend:", response.data);

      setResult(response.data.deepfake_result.result);
      setConfidence(response.data.deepfake_result.confidence);
      setMediaType(response.data.media_type);

      if (response.data.media_type === 'video') {
        setEmotionResult(response.data.emotion_result);
      } else {
        setEmotionResult(null);
      }

      // Pass the analyzed file data, including media type, to the parent component
      onFileAnalyzed({
        file: selectedFile,
        name: selectedFile.name,
        type: response.data.media_type,  // Use media_type from backend
        result: response.data.deepfake_result.result,
        confidence: response.data.deepfake_result.confidence,
        emotion_result: response.data.emotion_result,
      });
    } catch (error) {
      console.error('Error during detection:', error);
      setResult('Error during detection');
      setConfidence('N/A');
      setEmotionResult('N/A');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setMediaType(null);
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

          {!selectedFile && (
            <div {...getRootProps()} className={`mt-4 p-6 border-2 border-dashed rounded cursor-pointer ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-100'}`}>
              <input {...getInputProps()} />
              <p className="text-gray-600">Drag & drop a file here, or click to select a file</p>
            </div>
          )}

          {selectedFile && (
            <div className="mt-4">
              <p className="text-base-content mb-2">Preview:</p>
              {mediaType === 'image' ? (
                <img src={URL.createObjectURL(selectedFile)} alt="Preview" className="w-full h-64 object-cover rounded" />
              ) : (
                <video src={URL.createObjectURL(selectedFile)} controls className="w-full h-64 rounded" />
              )}
              <button
                onClick={result === null ? handleSubmit : handleReset}
                className={`mt-4 w-full py-2 px-4 ${result === null ? 'bg-green-500' : 'bg-blue-500'} text-white font-semibold rounded ${loading ? 'cursor-not-allowed' : ''}`}
                disabled={loading}
              >
                {loading ? 'Detecting...' : result === null ? 'Analyze Media' : 'Upload Another File'}
              </button>
            </div>
          )}

          {loading && <Loader filename={selectedFile.name} isComplete={result !== null} />}

          {result !== null && (
            <div className="mt-6">
              <h3 className="text-xl font-semibold text-base-content">Detection Result</h3>
              <p className="text-base-content mt-2">Result: <strong>{result}</strong></p>
              <p className="text-base-content mt-1">Confidence: <strong>{confidence}%</strong></p>
              <p className="text-base-content mt-1">Media Type: <strong>{mediaType}</strong></p>
              {mediaType === 'video' && emotionResult && (
                <div className="mt-4">
                  <p>Emotion: <strong>{emotionResult.emotion}</strong></p>
                  <p>Score: <strong>{emotionResult.score}</strong></p>
                  <p>Transcribed Text: <strong>{emotionResult.transcribed_text}</strong></p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
