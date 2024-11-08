import React, { useState, useEffect } from "react";

export default function Loader({ filename, isComplete }) {
  const [progress, setProgress] = useState(0);
  const [estimatedTime, setEstimatedTime] = useState(0);

  useEffect(() => {
    if (!filename) {
      console.error("Filename is not provided");
      return; // Early return if filename is not provided
    }

    // Open a connection to listen to the server-sent events
    const eventSource = new EventSource(`http://localhost:5000/progress/${filename}`);
    
    eventSource.onmessage = (event) => {
      const [rawProgress, rawEstimatedTime] = event.data.split(",");
      const progressValue = parseFloat(rawProgress);
      const estimatedTimeValue = parseFloat(rawEstimatedTime);

      // Cap the progress at 90% if detection is not yet complete
      if (!isComplete) {
        setProgress(Math.min(progressValue, 90));
      } else {
        // When detection is complete, set progress to 100%
        setProgress(100);
      }

      setEstimatedTime(estimatedTimeValue);
    };

    return () => {
      eventSource.close();
    };
  }, [filename, isComplete]);

  return (
    <div className="loader-container">
      <p>Processing... {progress}% completed</p>
      <progress value={progress} max="100"></progress>
      <p>Estimated time left: {Math.max(estimatedTime, 0).toFixed(1)} seconds</p>
    </div>
  );
}
