chrome.commands.onCommand.addListener(async (command) => {
  if (command === "save-jd") {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.id) return;

    const injectionResults = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => window.getSelection()?.toString() || ""
    });

    const selectedText = injectionResults[0]?.result;
    if (!selectedText) return;

    const formData = new FormData();
    formData.append("raw_text", selectedText);

    try {
      const response = await fetch("http://localhost:8000/api/v1/jd/jd-format-ollama", {
        method: "POST",
        body: formData
      });

      if (!response.ok) throw new Error("Backend error");

      const data = await response.json();

      if (data.status === "success") {
        let safeName = String(data.filename)
          .replace(/["']/g, "")
          .replace(/[\x00-\x1f\x7f-\x9f]/g, "")
          .trim();

        const cleanBase64 = data.file_content_b64.replace(/\s/g, '');

        chrome.downloads.download({
          url: `data:text/plain;base64,${cleanBase64}`,
          filename: safeName,
          saveAs: false
        }, (downloadId) => {
          if (chrome.runtime.lastError) {
            console.error("Download Error:", chrome.runtime.lastError.message);
            
            chrome.downloads.download({
              url: `data:text/plain;base64,${cleanBase64}`,
              filename: "job_description.txt"
            });
          }
        });
      }

    } catch (error) {
      console.error("Extension Error:", error);
    }
  }
});