import { useEffect, useState } from "react";
import AOS from "aos";
import "aos/dist/aos.css";
import Analysis from "../ScanPage/Analysis";
import myImage from "../../images/detection.jpg";

export default function Projects() {
  const [history, setHistory] = useState([]); // State to track file history

  useEffect(() => {
    AOS.init({ duration: 2000 });
  }, []);

  // Callback to add a new file to history
  const handleFileAnalyzed = (fileData) => {
    // Add file type information to the file data
    const newFileData = {
      ...fileData,
    };

    // Update history state
    setHistory((prevHistory) => [...prevHistory, newFileData]);
  };

  return (
    <div id="projects" className="mx-auto max-w-7xl px-6 py-24 lg:px-8">
      <h2 className="text-lg leading-7">Detect Media</h2>
      <p className="mt-2 text-4xl font-bold tracking-tight sm:text-6xl">DeepFake</p>

      <div className="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* History List */}
        <div className="col-span-1">
        {history.length > 0 ? (
          <div>
            <h3 className="text-2xl font-bold mb-4">Analysis History</h3>
            <ul className="space-y-2">
              {history.map((file, index) => (
                <li key={index} className="p-2 bg-base-200 rounded-lg shadow-sm flex flex-col">
                  <span className="font-semibold">{file.name}</span>
                  <span>Result: <strong>{file.result}</strong></span>
                  <span>Confidence: <strong>{file.confidence}%</strong></span>
                  <span>Emotion Analysis: <strong>{file.emotion_result ? `${file.emotion_result.emotion} (Score: ${file.emotion_result.score})` : 'N/A'}</strong></span>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <div>
            <img
              className="w-full ring-2 ring-base-300 max-w-none rounded-xl shadow-xl"
              src={myImage}
              alt="Detection"
            />
          </div>
        )}
        </div>

        {/* Analysis Component - Displayed Horizontally Next to History List */}
        <div className="col-span-1">
          <Analysis onFileAnalyzed={handleFileAnalyzed} />
        </div>
      </div>
    </div>
  );
}
