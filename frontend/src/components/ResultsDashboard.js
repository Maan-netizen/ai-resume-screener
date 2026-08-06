import React from "react";

function scoreColor(score) {
  if (score >= 70) return "#4ade80";
  if (score >= 40) return "#facc15";
  return "#f87171";
}

function ResultsDashboard({ result }) {
  const { score, matched_skills, missing_skills, filename } = result;

  return (
    <div className="card">
      <h2 style={{ marginBottom: "16px" }}>Results for "{filename}"</h2>

      <div
        className="score-circle"
        style={{ borderColor: scoreColor(score) }}
      >
        {score}%
      </div>

      <div className="skills-section">
        <div>
          <label>Matched Skills</label>
          {matched_skills.length === 0 && <p>None found</p>}
          {matched_skills.map((skill) => (
            <span key={skill} className="skill-tag matched">
              {skill}
            </span>
          ))}
        </div>
        <div>
          <label>Missing Skills</label>
          {missing_skills.length === 0 && <p>None — great match!</p>}
          {missing_skills.map((skill) => (
            <span key={skill} className="skill-tag missing">
              {skill}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ResultsDashboard;
