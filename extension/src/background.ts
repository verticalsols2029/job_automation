chrome.commands.onCommand.addListener(async (command) => {
  if (command === "save-jd") {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab.id) return;

    const jobUrl = tab.url || "URL not available";

    const injectionResults = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => window.getSelection()?.toString() || ""
    });

    const selectedText = injectionResults[0]?.result;

    if (!selectedText) {
      console.log("Nothing is highlighted!");
      return;
    }

    const formData = new FormData();
    formData.append("raw_text", selectedText);

    try {
      const response = await fetch("http://localhost:8000/api/v1/jd/jd-extract-gemini", {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      const formattedText = `Title: ${data.title}\nCompany: ${data.company}\nJob Link: ${jobUrl}\n\nJob Description:\n\n${selectedText}`;

      const safeTitle = (data.title !== "Not Found" ? data.title : "").replace(/[^a-z0-9_]/gi, '_');
      const safeCompany = (data.company !== "Not Found" ? data.company : "").replace(/[^a-z0-9_]/gi, '_');

      const base64Content = btoa(unescape(encodeURIComponent(formattedText)));
      const dataUrl = `data:text/plain;base64,${base64Content}`;

      chrome.downloads.download({
        url: dataUrl,
        filename: `${safeCompany}_${safeTitle}.txt`,
        saveAs: false 
      });

    } catch (error) {
      console.error("Failed to connect to backend:", error);
    }
  }
});