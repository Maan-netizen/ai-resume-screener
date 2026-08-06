import React from "react";

function History({ items }) {
  if (!items || items.length === 0) return null;

  return (
    <div className="card">
      <h2 style={{ marginBottom: "12px" }}>Recent Scans</h2>
      {items.map((item) => (
        <div className="history-item" key={item._id}>
          <span>{item.filename}</span>
          <span>{item.score}%</span>
        </div>
      ))}
    </div>
  );
}

export default History;
