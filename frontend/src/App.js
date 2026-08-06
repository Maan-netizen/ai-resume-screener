import React, { useState, useEffect } from "react";
import axios from "axios";
import UploadForm from "./components/UploadForm";
import ResultsDashboard from "./components/ResultsDashboard";
import History from "./components/History";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:5000";

function App() {
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/history`);
      setHistory(res.data);
    } catch (err) {
      console.error("Failed to load history", err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleScan = async (resumeFile, jobDescription) => {
    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_description", jobDescription);

    try {
      const res = await axios.post(`${API_BASE}/api/scan`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
      fetchHistory();
    } catch (err) {
      setError(err.response?.data?.error || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">AI Resume Screener</h1>
      <p className="subtitle">
        Upload a resume and a job description to get a match score and
        skill-gap analysis.
      </p>

      <UploadForm onScan={handleScan} loading={loading} />

      {error && <p className="error">{error}</p>}

      {result && <ResultsDashboard result={result} />}

      <History items={history} />
    </div>
  );
}

export default App;
