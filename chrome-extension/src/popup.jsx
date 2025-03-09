import React, { useState } from "react";
import ReactDOM from "react-dom";

function Popup() {
  const [status, setStatus] = useState("Enter a sentence to check its truthfulness.");
  const [sentence, setSentence] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSentenceChange = (event) => {
    setSentence(event.target.value);
  };

  const handleCheckTruthfulness = async () => {
    if (!sentence.trim() || sentence.trim().length < 5) {
      setStatus("Please enter a meaningful sentence (at least 5 characters).");
      return;
    }

    setIsLoading(true);
    setStatus("Analyzing sentence...");

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (!tabs || tabs.length === 0) {
        setIsLoading(false);
        setStatus("No active tab found to send the request.");
        return;
      }

      chrome.tabs.sendMessage(
        tabs[0].id,
        { action: "analyseSentenceRequest", sentence },
        (response) => {
          setIsLoading(false);
          if (!response) {
            setStatus("Error: No response from the server. Please try again.");
            return;
          }

          if (response.label === "ERROR") {
            setStatus("Analysis failed! Check console for more details.");
          } else {
            const truthfulness = response.label === "REAL" ? "Truthful" : "Likely Fake";
            setStatus(`Analysis complete! Truthfulness: ${truthfulness}`);
          }
        }
      );
    });
  };

  return (
    <div style={{ padding: "20px", textAlign: "center", fontFamily: "Arial, sans-serif", backgroundColor: "#f7f7f7" }}>
      <h1 style={{ fontSize: "20px", marginBottom: "20px" }}>Fact Checker</h1>
      <textarea
        style={{ width: "100%", padding: "10px", marginBottom: "15px", borderRadius: "5px", border: "1px solid #ccc" }}
        rows="3"
        placeholder="Enter a sentence to check..."
        value={sentence}
        onChange={handleSentenceChange}
      />
      <button
        style={{
          backgroundColor: isLoading ? "#ccc" : "#007bff",
          color: "#fff",
          border: "none",
          padding: "12px 24px",
          fontSize: "16px",
          borderRadius: "5px",
          cursor: isLoading ? "not-allowed" : "pointer",
        }}
        onClick={handleCheckTruthfulness}
        disabled={isLoading}
      >
        {isLoading ? "Checking..." : "Check Truthfulness"}
      </button>
      {isLoading && <p style={{ color: "#007bff", fontSize: "14px" }}>Processing...</p>}
      <p style={{ marginTop: "15px", fontSize: "14px", color: "#333" }}>{status}</p>
    </div>
  );
}

ReactDOM.render(<Popup />, document.getElementById("root"));
