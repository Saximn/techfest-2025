import React, { useState } from "react";
import ReactDOM from "react-dom";

function Popup() {
  const [status, setStatus] = useState(
    "Click the button to analyze the article"
  );

  const handleAnalyze = () => {
    setStatus("Analyzing...");
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.sendMessage(
        tabs[0].id,
        { action: "highlightFakeNews" },
        (response) => {
          if (response && response.done) {
            setStatus("Analysis complete!");
          } else {
            setStatus("Failed to analyze content.");
          }
        }
      );
    });
  };

  const containerStyle = {
    padding: "20px",
    textAlign: "center",
    fontFamily: "Arial, sans-serif",
    backgroundColor: "#f7f7f7",
  };

  const headingStyle = {
    fontSize: "20px",
    marginBottom: "20px",
  };

  const buttonStyle = {
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    padding: "12px 24px",
    fontSize: "16px",
    borderRadius: "5px",
    cursor: "pointer",
  };

  const statusStyle = {
    marginTop: "15px",
    fontSize: "14px",
    color: "#333",
  };

  return (
    <div style={containerStyle}>
      <h1 style={headingStyle}>BERT-LIME Fact Checker</h1>
      <button style={buttonStyle} onClick={handleAnalyze}>
        Analyze Article
      </button>
      <p style={statusStyle}>{status}</p>
    </div>
  );
}

ReactDOM.render(<Popup />, document.getElementById("root"));
