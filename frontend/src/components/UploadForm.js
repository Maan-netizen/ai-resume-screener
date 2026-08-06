import React, { useState } from "react";

function UploadForm({ onScan, loading }) {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file || !jobDescription.trim()) return;
    onScan(file, jobDescription);
  };

  return (
    <form className="card" onSubmit={handleSubmit}>
      <label>Resume (PDF, DOCX, or TXT)</label>
      <div
        className="file-drop"
        onClick={() => document.getElementById("resumeInput").click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
      >
        <input
          id="resumeInput"
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleFileChange}
        />
        <p>Click or drag a file here to upload</p>
        {file && <p className="file-name">{file.name}</p>}
      </div>

      <label style={{ marginTop: "20px" }}>Job Description</label>
      <textarea
        placeholder="Paste the job description here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />

      <button
        type="submit"
        className="primary"
        disabled={loading || !file || !jobDescription.trim()}
      >
        {loading ? "Scanning..." : "Scan Resume"}
      </button>
    </form>
  );
}

export default UploadForm;
