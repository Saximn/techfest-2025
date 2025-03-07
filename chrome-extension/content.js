async function highlightFakeNews() {
  // Select all <p> elements on the page
  const paragraphs = document.querySelectorAll("p");
  for (const p of paragraphs) {
    const originalText = p.innerText.trim();
    if (!originalText) continue;
    // Split paragraph into sentences using regex
    const sentences = originalText.match(/[^.!?]+[.!?]+[\])'"`’”]*|.+/g);
    if (!sentences) continue;

    // Classify each sentence in parallel
    const classificationPromises = sentences.map((sentence) =>
      fetch("http://localhost:5000/classify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: sentence }),
      })
        .then((response) => response.json())
        .then((data) => ({ sentence, label: data.label, score: data.score }))
        .catch((error) => {
          console.error("Error classifying sentence:", error);
          return { sentence, label: "UNKNOWN", score: 0 };
        })
    );

    const results = await Promise.all(classificationPromises);

    // Create a new paragraph element to hold the highlighted sentences
    const newParagraph = document.createElement("p");
    results.forEach((result) => {
      const span = document.createElement("span");
      span.textContent = result.sentence + " "; // Preserve spacing
      const label = result.label.toUpperCase();
      const score = result.score;

      // Set background color based on classification:
      // - "FAKE" with score >= 0.8 => light red (high risk)
      // - "FAKE" with score >= 0.5 => light orange (medium risk)
      // - "PROVOCATIVE" => light magenta
      if (label === "FAKE") {
        if (score >= 0.8) {
          span.style.backgroundColor = "lightcoral";
        } else if (score >= 0.5) {
          span.style.backgroundColor = "#FFD580";
        }
      } else if (label === "PROVOCATIVE") {
        span.style.backgroundColor = "#FFB3FF";
      }
      newParagraph.appendChild(span);
    });
    p.replaceWith(newParagraph);
  }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "highlightFakeNews") {
    highlightFakeNews().then(() => sendResponse({ done: true }));
    return true; // Keep messaging channel open for async operations
  }

  // Optional: add a listener for Google Fact Check if needed.
});
