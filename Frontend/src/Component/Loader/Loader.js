import React, { useState, useEffect } from "react";

export default function Loader({ filename }) {
  const [progress, setProgress] = useState(0);
  const [estimatedTime, setEstimatedTime] = useState(0);

  useEffect(() => {
    if (!filename) {
      console.error("Filename is not provided");
      return; // Early return if filename is not provided
    }

    fetch(`http://localhost:5000/progress/${filename}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      })
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.error('Error fetching progress:', error);
      });
      
    const eventSource = new EventSource(`http://localhost:5000/progress/${filename}`);
    eventSource.onmessage = (event) => {
      const [progress, estimatedTime] = event.data.split(",");
      setProgress(progress);
      setEstimatedTime(estimatedTime);
    };

    return () => {
      eventSource.close();
    };
  }, [filename]);

  return (
    <div className="loader-container">
      <p>Processing... {progress}% completed</p>
      <progress value={progress} max="100"></progress>
      <p>Estimated time left: {Math.max(estimatedTime, 0).toFixed(1)} seconds</p>
    </div>
  );
}
