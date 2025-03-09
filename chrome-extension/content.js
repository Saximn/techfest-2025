// content.js
async function analyseSentence(sentence) {
  console.log("analyseSentence function called with:", sentence);
  try {
    const response = await fetch("http://localhost:5000/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: sentence }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Server error! Status: ${response.status}, Response: ${errorText}`);
      throw new Error(`HTTP error! Status: ${response.status}, Response: ${errorText}`);
    }

    // Validate if response is JSON
    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      throw new Error("Invalid response format from server");
    }

    const data = await response.json();
    if (!data.label || typeof data.score === "undefined") {
      throw new Error("Invalid response: Missing 'label' or 'score'");
    }

    return { label: data.label, score: data.score };
  } catch (error) {
    console.error("Error in analyseSentence:", error);
    return { label: "ERROR", score: -1 }; // Graceful fallback for errors
  }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Message received:", message);

  if (message.action === "analyseSentenceRequest") {
    analyseSentence(message.sentence)
      .then(result => sendResponse(result))
      .catch(error => {
        console.error("Unhandled error in analyseSentence:", error);
        sendResponse({ label: "ERROR", score: -1 });
      });

    return true; // Keeps sendResponse valid for async calls
  }
});
