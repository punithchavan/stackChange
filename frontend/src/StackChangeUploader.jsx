import { useEffect, useState } from 'react';
import axios from 'axios';
import bgVideo from './assets/bgVideo.mp4';
export default function StackChangeUploader() {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('');
  const [jobId, setJobId] = useState(null); // <-- Add this line


  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      setFile(droppedFile);
      setMessage('');
      setProgress(0);
    }
  };

  const handleDragOver = (e) => e.preventDefault();

  const handleChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      console.log("📥 File selected from input:", selectedFile);
      setFile(selectedFile);
      setMessage('');
      setProgress(0);
    }
  };

 
const handleUpload = async () => {
  if (!file) {
    setMessage('❌ Please select a file first.');
    return;
  }

  setMessage('Uploading...');
  setProgress(0);

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post(
      'http://127.0.0.1:8000/upload/',
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setProgress(percentCompleted);
        },
      }
    );
    if (response.data.job_id) {
      setMessage(`✅ Upload successful! Job ID: ${response.data.job_id}`);
      setJobId(response.data.job_id); // <-- Save job ID for download
    } else {
      setMessage('✅ File uploaded, but no job ID returned.');
      setJobId(null);
    }
  } catch (error) {
    setMessage('❌ Upload failed.');
    setProgress(0);
    setJobId(null);
  }
};

  // Download handler
  const handleDownload = () => {
    if (!jobId) return;
    // Open download in a new tab/window
    window.open(`http://127.0.0.1:8000/download/${jobId}/`, '_blank');
  };



  return (
    <div className="position-relative">
      {/* 🎥 Background Video */}
      <video
        autoPlay
        muted
        loop
        className="position-fixed top-0 start-0 w-100 h-100 object-fit-cover z-n1"
      >
        <source src={bgVideo} type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      {/* Centered Content */}
      <div className="d-flex flex-column justify-content-center align-items-center vh-100 text-center">
        {/* 🏷️ Centered Heading */}
        <h1 className="text-light fw-bold mb-4" style={{ textShadow: '0 0 10px black' }}>
          StackChange
        </h1>

        {/* 📦 Upload Box */}
        <div
          className="bg-light bg-opacity-75 p-5 rounded shadow"
          style={{ width: '100%', maxWidth: '500px' }}
        >
          <h4 className="mb-4">Upload File</h4>

          {/* Drag & Drop */}
          <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            className="border border-primary rounded p-4 text-center mb-3"
            style={{ backgroundColor: "#f8f9fa", cursor: "pointer" }}
          >
            <p className="mb-1">Drag & drop a file here</p>
            <p className="text-muted small">or use the button below</p>
            {file && <p className="text-success mt-2 fs-4">📄 {file.name}</p>}

          </div>

          {/* File Input */}
          <div className="mb-3">
            {/* Creative File Input */}
<div className="mb-3 text-center">
  <input
    type="file"
    id="fileInput"
    style={{ display: "none" }}
    onChange={handleChange}
  />
  <label htmlFor="fileInput" className="btn btn-outline-secondary">
    📁 Choose a File
  </label>
</div>

          </div>

          {/* Upload Button */}
          <button className="btn btn-primary w-100" onClick={handleUpload}>
            Upload
          </button>

          {/* Download Button */}
          {jobId && (
            <button
              className="btn btn-success w-100 mt-3"
              onClick={handleDownload}
            >
              Download Converted File
            </button>
          )}

          {/* Progress Bar */}
{progress > 0 && (
  <div className="mt-4">
    <div className="progress" style={{ height: '25px', borderRadius: '50px', overflow: 'hidden' }}>
      <div
        className="progress-bar bg-success progress-bar-striped progress-bar-animated"
        role="progressbar"
        style={{
          width: `${progress}%`,
          fontWeight: 'bold',
          fontSize: '16px',
          transition: 'width 0.4s ease-in-out'
        }}
      >
        {progress}%
      </div>
    </div>
  </div>
)}


          {/* Upload Message */}
          {message && <div className="alert alert-info mt-3">{message}</div>}
        </div>
      </div>
    </div>
  );
}
